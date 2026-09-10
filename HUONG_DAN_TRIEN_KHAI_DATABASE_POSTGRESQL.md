# 📚 HƯỚNG DẪN CHI TIẾT CÁCH XÂY DỰNG & TÍCH HỢP POSTGRESQL DATABASE
> **Dự án**: Booking & Scheduling Management System  
> **Kiến trúc**: Clean Architecture & Repository Pattern  
> **Công nghệ**: Python 3.10+, FastAPI, SQLAlchemy 2.0 ORM, PostgreSQL 16, Docker  

---

## 📑 MỤC LỤC
1. [Triết Lý Thiết Kế & Kiến Trúc Clean Architecture](#1-triết-lý-thiết-kế--kiến-trúc-clean-architecture)
2. [Sơ Đồ Luồng Dữ Liệu (Architecture Diagram)](#2-sơ-đồ-luồng-dữ-liệu-architecture-diagram)
3. [Quy Trình 7 Bước Triển Khai Database Chi Tiết](#3-quy-trình-7-bước-triển-khai-database-chi-tiết)
   - [Bước 1: Khai báo Thư viện & Dependencies](#bước-1-khai-báo-thư-viện--dependencies)
   - [Bước 2: Cấu hình Biến Môi Trường & Settings](#bước-2-cấu-hình-biến-môi-trường--settings)
   - [Bước 3: Thiết lập SQLAlchemy Engine & Session Pool](#bước-3-thiết-lập-sqlalchemy-engine--session-pool)
   - [Bước 4: Thiết kế Data Model (ORM Model)](#bước-4-thiết-kế-data-model-orm-model)
   - [Bước 5: Triển khai Repository Pattern (Data Access Layer)](#bước-5-triển-khai-repository-pattern-data-access-layer)
   - [Bước 6: Dependency Injection & Quản lý Vòng Đời Tự Tạo Bảng](#bước-6-dependency-injection--quản-lý-vòng-đời-tự-tạo-bảng)
   - [Bước 7: Đóng gói Docker & Docker Compose](#bước-7-đóng-gói-docker--docker-compose)
4. [Hướng Dẫn Vận Hành & Thao Tác Thực Tế](#4-hướng-dẫn-vận-hành--thao-tác-thực-tế)
5. [Chiến Lược Kiểm Thử Database (Testing Strategy)](#5-chiến-lược-kiểm-thử-database-testing-strategy)
6. [Best Practices & Kinh Nghiệm Thực Tế](#6-best-practices--kinh-nghiệm-thực-tế)

---

## 1. Triết Lý Thiết Kế & Kiến Trúc Clean Architecture

Trong các dự án phần mềm chuyên nghiệp, việc gắn chặt mã nguồn logic nghiệp vụ (Business Logic) trực tiếp vào các câu lệnh SQL hoặc một hệ quản trị cơ sở dữ liệu cụ thể sẽ dẫn đến:
- ❌ Code bị phụ thuộc chặt chẽ vào hệ quản trị database cụ thể.
- ❌ Rất khó viết Unit Test (luôn phải kết nối DB thật, chạy chậm và dễ lỗi).
- ❌ Khi muốn chuyển từ lưu trữ File (JSON) sang PostgreSQL, MySQL, hay MongoDB thì phải viết lại toàn bộ code.

### 💡 Giải pháp: Áp dụng **Repository Pattern**
```
+----------------------------------------------------------------+
|                        API / CLI Layer                         |
+----------------------------------------------------------------+
                               |
                               v
+----------------------------------------------------------------+
|                 BookingService (Business Logic)                |
|           (Chỉ biết đến BaseBookingRepository Interface)       |
+----------------------------------------------------------------+
                               |
            +------------------+------------------+
            |                                     |
            v                                     v
+-----------------------+             +--------------------------+
| JSONBookingRepository |             | PostgresBookingRepository|
|    (File Storage)     |             |    (SQLAlchemy + Postgres)|
+-----------------------+             +--------------------------+
```

> [!NOTE]
> **Điểm mấu chốt**: Tầng `BookingService` và các API Router chỉ gọi các hàm định nghĩa trong `BaseBookingRepository` (`get_all`, `create`, `update`, `delete`). Do đó, khi ta chuyển từ JSON sang PostgreSQL, **100% logic nghiệp vụ và API code không cần thay đổi một dòng nào**.

---

## 2. Sơ Đồ Luồng Dữ Liệu (Architecture Diagram)

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client / User
    participant Router as FastAPI Router
    participant Service as BookingService
    participant Repo as PostgresBookingRepository
    participant Session as SQLAlchemy Session Local
    participant DB as PostgreSQL Database

    Client->>Router: POST /api/v1/bookings (JSON Payload)
    Router->>Service: create_booking(booking_in)
    Service->>Service: Validate nghiệp vụ (Check rỗng, trùng lặp...)
    Service->>Repo: create(booking_in)
    Repo->>Session: Khởi tạo DB Session & Mapping sang BookingModel
    Session->>DB: INSERT INTO bookings VALUES (...)
    DB-->>Session: Trả về record mới + ID tự tăng
    Session-->>Repo: Commit transaction & Refresh model
    Repo-->>Service: Chuyển đổi ORM Model -> BookingResponse (DTO)
    Service-->>Router: Trả về BookingResponse
    Router-->>Client: 201 Created (JSON Response)
```

---

## 3. Quy Trình 7 Bước Triển Khai Database Chi Tiết

### Bước 1: Khai báo Thư viện & Dependencies
Sử dụng **SQLAlchemy 2.0** (ORM tiêu chuẩn cao nhất của Python) và driver **psycopg2-binary** (giao tiếp hiệu năng cao với PostgreSQL).

Thêm vào file `requirements/base.txt` và `pyproject.toml`:
```text
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.9
```

Cài đặt vào môi trường ảo:
```bash
pip install -r requirements/base.txt
```

---

### Bước 2: Cấu hình Biến Môi Trường & Settings

Tại file `src/booking_app/core/config.py`:
- Định nghĩa các biến môi trường cấu hình PostgreSQL.
- Định nghĩa thuộc tính `sync_database_url` để tự động ghép connection string chuẩn định dạng: `postgresql://user:password@host:port/dbname`.
- Bổ sung cờ `DB_TYPE` (`"postgres"` hoặc `"json"`).

```python
import os
from typing import Optional
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Booking & Scheduling Management API")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Chọn chế độ lưu trữ: "postgres" | "json"
    DB_TYPE: str = os.getenv("DB_TYPE", "postgres").lower()

    # Cấu hình JSON
    DATA_FILE_PATH: str = os.getenv("DATA_FILE_PATH", "data/bookings.json")

    # Cấu hình PostgreSQL
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "123456")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "booking_db")
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    @property
    def sync_database_url(self) -> str:
        """Sinh ra URL kết nối chuẩn cho SQLAlchemy."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
```

Mẫu cấu hình trong `.env.example`:
```env
DB_TYPE="postgres"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="123456"
POSTGRES_SERVER="localhost"
POSTGRES_PORT=5432
POSTGRES_DB="booking_db"
DATABASE_URL="postgresql://postgres:123456@localhost:5432/booking_db"
```

---

### Bước 3: Thiết lập SQLAlchemy Engine & Session Pool

Tạo file `src/booking_app/db/session.py`:
- `create_engine`: Quản lý pool kết nối, thiết lập `pool_pre_ping=True` (tự động phát hiện và phục hồi kết nối bị đứt ngầm).
- `sessionmaker`: Nhà máy sản xuất Session theo mỗi transaction.
- `get_db_session()`: Context Manager tự động `commit()` khi hoàn thành và `rollback()` khi có ngoại lệ, đảm bảo an toàn tuyệt đối chống rò rỉ kết nối (Connection Leak).
- `init_db()`: Hàm tự động tạo bảng qua `Base.metadata.create_all(bind=engine)`.

```python
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from booking_app.core.config import settings

Base = declarative_base()

engine_kwargs = {"pool_pre_ping": True}
if settings.sync_database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update({"pool_size": 10, "max_overflow": 20})

engine = create_engine(settings.sync_database_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager cấp phát và thu hồi session an toàn."""
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db(target_engine=None):
    """Tự động khởi tạo toàn bộ bảng trong DB nếu chưa có."""
    import booking_app.models.booking  # Đảm bảo metadata được nạp
    eng = target_engine or engine
    Base.metadata.create_all(bind=eng)
```

---

### Bước 4: Thiết kế Data Model (ORM Model)

Tạo file `src/booking_app/models/booking.py`:
- Đại diện cho bảng vật lý `bookings` trong cơ sở dữ liệu.
- Chứa phương thức `.to_schema()` để chuyển đổi sạch từ SQLAlchemy ORM Entity sang Pydantic DTO (`BookingResponse`).

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text
from booking_app.db.session import Base
from booking_app.schemas.booking import BookingStatus, BookingResponse

class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer = Column(String(100), nullable=False, index=True)
    service = Column(String(100), nullable=False)
    time = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default=BookingStatus.CONFIRMED.value, nullable=False)
    created_at = Column(String(50), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nullable=False)

    def to_schema(self) -> BookingResponse:
        """Chuyển đổi sang Pydantic Schema chuẩn hóa."""
        return BookingResponse(
            id=self.id,
            customer=self.customer,
            service=self.service,
            time=self.time,
            notes=self.notes,
            status=BookingStatus(self.status) if isinstance(self.status, str) else self.status,
            created_at=str(self.created_at),
        )
```

---

### Bước 5: Triển khai Repository Pattern (Data Access Layer)

Tạo file `src/booking_app/repositories/postgres_repository.py`:
- Kế thừa lớp trừu tượng `BaseBookingRepository`.
- Thực thi toàn bộ các thao tác: `get_all`, `get_by_id`, `create`, `update`, `delete` qua ORM.

```python
from contextlib import contextmanager
from typing import List, Optional, Callable, Generator
from sqlalchemy.orm import Session
from booking_app.repositories.base import BaseBookingRepository
from booking_app.schemas.booking import BookingResponse, BookingCreate, BookingUpdate, BookingStatus
from booking_app.models.booking import BookingModel
from booking_app.db.session import SessionLocal

class PostgresBookingRepository(BaseBookingRepository):
    """Triển khai lưu trữ lịch hẹn bằng cơ sở dữ liệu PostgreSQL."""

    def __init__(self, session_factory: Optional[Callable[[], Session]] = None):
        self.session_factory = session_factory or SessionLocal

    @contextmanager
    def _get_session(self) -> Generator[Session, None, None]:
        session: Session = self.session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_all(self) -> List[BookingResponse]:
        with self._get_session() as session:
            records = session.query(BookingModel).order_by(BookingModel.id.asc()).all()
            return [rec.to_schema() for rec in records]

    def get_by_id(self, booking_id: int) -> Optional[BookingResponse]:
        with self._get_session() as session:
            record = session.query(BookingModel).filter(BookingModel.id == booking_id).first()
            return record.to_schema() if record else None

    def create(self, booking: BookingCreate) -> BookingResponse:
        with self._get_session() as session:
            db_booking = BookingModel(
                customer=booking.customer,
                service=booking.service,
                time=booking.time,
                notes=booking.notes,
                status=BookingStatus.CONFIRMED.value,
            )
            session.add(db_booking)
            session.commit()
            session.refresh(db_booking)
            return db_booking.to_schema()

    def update(self, booking_id: int, booking_update: BookingUpdate) -> Optional[BookingResponse]:
        with self._get_session() as session:
            record = session.query(BookingModel).filter(BookingModel.id == booking_id).first()
            if not record:
                return None
            
            update_data = booking_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if value is not None:
                    if hasattr(value, "value"):
                        value = value.value
                    setattr(record, field, value)
            
            session.commit()
            session.refresh(record)
            return record.to_schema()

    def delete(self, booking_id: int) -> bool:
        with self._get_session() as session:
            record = session.query(BookingModel).filter(BookingModel.id == booking_id).first()
            if not record:
                return False
            session.delete(record)
            session.commit()
            return True
```

---

### Bước 6: Dependency Injection & Quản lý Vòng Đời Tự Tạo Bảng

#### 1. Cấu hình cấp phát trong `src/booking_app/api/deps.py`:
```python
from functools import lru_cache
from booking_app.core.config import settings
from booking_app.repositories.base import BaseBookingRepository
from booking_app.repositories.json_repository import JSONBookingRepository
from booking_app.repositories.postgres_repository import PostgresBookingRepository
from booking_app.services.booking_service import BookingService

@lru_cache()
def get_repository() -> BaseBookingRepository:
    """Tự động cấp phát Repository phù hợp cấu hình."""
    if settings.DB_TYPE == "postgres":
        return PostgresBookingRepository()
    return JSONBookingRepository(file_path=settings.DATA_FILE_PATH)

def get_booking_service() -> BookingService:
    repo = get_repository()
    return BookingService(repository=repo)
```

#### 2. Tự động kiểm tra và tạo bảng qua FastAPI `lifespan` trong `src/booking_app/main.py`:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from booking_app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.DB_TYPE == "postgres":
        try:
            from booking_app.db.session import init_db
            init_db()
        except Exception as e:
            print(f"⚠️ Cảnh báo khởi tạo bảng DB: {e}")
    yield

def create_app() -> FastAPI:
    return FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
```

---

### Bước 7: Đóng gói Docker & Docker Compose

Tại file `docker-compose.yml`:
- Thiết lập service PostgreSQL `db` với image `postgres:16-alpine`.
- Cơ chế `healthcheck` qua lệnh `pg_isready`.
- API Server sẽ chờ cho tới khi PostgreSQL hoàn toàn sẵn sàng (`condition: service_healthy`).
- Dữ liệu được lưu an toàn trong Docker Volume `postgres_data`.

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    container_name: booking_postgres_db
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-123456}
      POSTGRES_DB: ${POSTGRES_DB:-booking_db}
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-booking_db}"]
      interval: 5s
      timeout: 5s
      retries: 5

  booking-api:
    build: .
    container_name: booking_management_api
    ports:
      - "${PORT:-8000}:8000"
    volumes:
      - ./data:/app/data
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - DB_TYPE=postgres
      - DATABASE_URL=postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-123456}@db:5432/${POSTGRES_DB:-booking_db}
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## 4. Hướng Dẫn Vận Hành & Thao Tác Thực Tế

### Cách 1: Chạy Siêu Tốc Bằng Docker Compose (Khuyên dùng)
Chỉ với 1 câu lệnh duy nhất:
```bash
docker compose up -d --build
```
Hệ thống sẽ:
1. Kéo image `postgres:16-alpine` về và khởi động DB container.
2. Tự động kiểm tra cho đến khi PostgreSQL sẵn sàng tiếp nhận kết nối.
3. Build API container, kết nối vào DB, tự động khởi tạo bảng `bookings`.
4. Mở cổng `8000` phục vụ API.

Xem Swagger UI: **http://localhost:8000/docs**

---

### Cách 2: Chạy Trên Máy Cục Bộ (Local Machine)
1. Cài đặt các package cần thiết:
   ```bash
   pip install -r requirements/dev.txt
   ```
2. Khởi tạo bảng cơ sở dữ liệu:
   ```bash
   python init_db.py
   ```
3. Chạy API Server:
   ```bash
   python run_api.py
   ```
4. Chạy Giao diện Dòng lệnh (CLI):
   ```bash
   python run_cli.py
   ```

---

## 5. Chiến Lược Kiểm Thử Database (Testing Strategy)

Một trong những sai lầm phổ biến khi viết test cho Database là yêu cầu phải có một server PostgreSQL thật đang chạy trên máy của lập trình viên hoặc trên CI/CD runner.

### 💡 Giải pháp Test siêu tốc: **SQLite In-Memory Mock**
Nhờ việc sử dụng SQLAlchemy ORM trừu tượng, ta tạo một Pytest Fixture trong `tests/conftest.py` sử dụng `sqlite:///:memory:` để giả lập cơ sở dữ liệu quan hệ với tốc độ miligiây:

```python
@pytest.fixture
def test_postgres_repo():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from booking_app.db.session import Base
    from booking_app.repositories.postgres_repository import PostgresBookingRepository
    import booking_app.models.booking  # noqa: F401

    # Tạo DB tạm trong RAM cho từng test case
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    repo = PostgresBookingRepository(session_factory=testing_session_local)
    yield repo
    Base.metadata.drop_all(bind=engine)
```

Chạy kiểm thử:
```bash
pytest -v
```

---

## 6. Best Practices & Kinh Nghiệm Thực Tế

1. **Luôn sử dụng Context Manager cho Database Session**: Tránh gọi `session = SessionLocal()` trần trụi mà không có `try...finally: session.close()`. Context Manager đảm bảo kết nối luôn được trả về pool dù chương trình có phát sinh lỗi.
2. **Index hợp lý trên các cột thường xuyên tìm kiếm**: Thêm `index=True` cho cột `customer` và `id` trong `BookingModel` giúp tăng tốc độ truy vấn khi dữ liệu lớn.
3. **Connection Pooling**: Đặt `pool_pre_ping=True` giúp tránh lỗi kinh điển `OperationalError: SSL SYSCALL error` hoặc `Server closed connection unexpectedly` khi kết nối PostgreSQL bị nhàn rỗi (idle timeout).
4. **Phân tách DTO (Pydantic) và ORM Model (SQLAlchemy)**: Không bao giờ trả trực tiếp instance ORM Model ra API response. Luôn chuyển đổi sang Pydantic DTO (`to_schema()`) để kiểm soát dữ liệu đầu ra và tránh lỗi tuần tự hóa (Serialization error / Lazy loading error).
