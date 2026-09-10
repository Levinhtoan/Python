# 📅 Booking & Scheduling Management System

Dự án mẫu quản lý đặt lịch hẹn thực tế được xây dựng theo kiến trúc **Clean Architecture** và chuẩn **`src-layout`** chuẩn mực của Python Packaging (tham khảo [PYTHON_PROJECT_STRUCTURE.md](file:///e:/Booking-SchedulingManagement/PYTHON_PROJECT_STRUCTURE.md)).

---

## 🌟 Tính Năng Chính

- **Hỗ trợ Đa Cơ Sở Dữ Liệu (Multi-Database Support)**:
  - 🐘 **PostgreSQL (SQLAlchemy 2.0 ORM)**: Lưu trữ chuẩn enterprise qua cơ sở dữ liệu quan hệ mạnh mẽ.
  - 📁 **JSON File Storage**: Lưu trữ file phẳng gọn nhẹ phù hợp môi trường phát triển thử nghiệm nhanh.
  - Chuyển đổi linh hoạt giữa các bộ lưu trữ chỉ với biến môi trường `DB_TYPE="postgres"` hoặc `DB_TYPE="json"`.
- **RESTful API (FastAPI)**: Đầy đủ CRUD đặt lịch, hủy lịch, xem danh sách và Swagger UI interactive docs (`/docs`).
- **Giao diện CLI Console**: Menu console trực quan tương tác trực tiếp với tầng Service.
- **Phân tầng Clean Architecture**:
  - `schemas`: DTO / Data Validation với Pydantic v2.
  - `models`: SQLAlchemy ORM Model ánh xạ bảng `bookings`.
  - `repositories`: Trừu tượng hóa việc lưu trữ (`BaseBookingRepository`, `PostgresBookingRepository`, `JSONBookingRepository`).
  - `services`: Xử lý toàn bộ logic nghiệp vụ (Business logic độc lập).
  - `api`: Fast, clean routing và dependency injection.
- **Kiểm thử tự động (Pytest)**: Unit tests cho Service Layer, Repository Layer (Postgres/SQLite in-memory) và Integration tests cho API endpoints.
- **Docker & Docker Compose**: Đóng gói hoàn chỉnh API và PostgreSQL Container (`postgres:16-alpine`), tự động tạo volume và kiểm tra sức khỏe (healthcheck).

---

## 📂 Cấu Trúc Dự Án

```text
Booking-SchedulingManagement/
├── .github/workflows/tests.yml   # CI/CD Tự động chạy Unit Test
├── data/bookings.json            # File lưu trữ dữ liệu (khi dùng JSON)
├── requirements/
│   ├── base.txt                  # Thư viện runtime chính (FastAPI, SQLAlchemy, psycopg2, ...)
│   └── dev.txt                   # Thư viện cho môi trường dev & test (pytest, httpx, ruff, ...)
├── src/
│   └── booking_app/
│       ├── api/                  # Tầng giao tiếp HTTP (Routers, Endpoints, Deps)
│       ├── core/                 # Cấu hình hệ thống (Settings, Custom Exceptions)
│       ├── db/                   # Cấu hình kết nối Database & Session (SQLAlchemy)
│       ├── models/               # SQLAlchemy ORM Models
│       ├── schemas/              # Pydantic Schemas & DTOs
│       ├── repositories/         # Tầng lưu trữ dữ liệu (Repository Pattern)
│       │   ├── base.py           # Interface trừu tượng
│       │   ├── json_repository.py # Repository cho JSON File
│       │   └── postgres_repository.py # Repository cho PostgreSQL
│       ├── services/             # Tầng nghiệp vụ cốt lõi (Business Logic)
│       ├── main.py               # Entrypoint FastAPI Server
│       └── cli.py                # Entrypoint Giao diện dòng lệnh
├── tests/
│   ├── conftest.py               # Fixtures dùng chung cho pytest (JSON & SQLite in-memory DB)
│   ├── unit/                     # Unit test cho Service Layer & Postgres Repository
│   └── integration/              # Integration test cho API Routes
├── .env.example                  # Template biến môi trường (PostgreSQL / JSON)
├── Dockerfile & docker-compose.yml # Cấu hình container API + PostgreSQL
├── pyproject.toml                # Cấu hình dự án & Pytest
├── init_db.py                    # Script thủ công tạo bảng cơ sở dữ liệu
├── run_api.py                    # Script chạy nhanh FastAPI server
└── run_cli.py                    # Script chạy nhanh CLI console
```

---

## ⚙️ Cấu Hình Môi Trường (.env)

Tạo file `.env` từ `.env.example`:
```bash
cp .env.example .env
```

### Sử dụng với PostgreSQL (Khuyến nghị):
```env
DB_TYPE="postgres"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="123456"
POSTGRES_SERVER="localhost"
POSTGRES_PORT=5432
POSTGRES_DB="booking_db"
DATABASE_URL="postgresql://postgres:123456@localhost:5432/booking_db"
```

### Hoặc chuyển sang JSON File Storage:
```env
DB_TYPE="json"
DATA_FILE_PATH="data/bookings.json"
```

---

## 🚀 Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Kích hoạt môi trường ảo (Virtual Environment)
```bash
# Trên Windows:
.\venv\Scripts\activate

# Trên Linux/macOS:
source venv/bin/activate
```

### 2. Cài đặt thư viện
```bash
pip install -r requirements/dev.txt
```

### 3. Khởi tạo bảng Database (Khi dùng PostgreSQL)
API Server sẽ tự động khởi tạo bảng khi khởi động (`lifespan`). Bạn cũng có thể chủ động khởi tạo thủ công:
```bash
python init_db.py
```

### 4. Chạy API Server
```bash
python run_api.py
```
- Swagger API Docs: **http://127.0.0.1:8000/docs**
- ReDoc Docs: **http://127.0.0.1:8000/redoc**
- Trang chủ API: **http://127.0.0.1:8000/**

### 5. Chạy Giao diện CLI Console
```bash
python run_cli.py
```

### 6. Chạy Toàn Bộ Kiểm Thử (Pytest)
```bash
pytest -v
```

---

## 🐳 Khởi Chạy Nhanh Với Docker Compose (API + PostgreSQL)

Khởi động đồng thời cả cơ sở dữ liệu PostgreSQL và API Server chỉ bằng một lệnh:
```bash
docker compose up -d --build
```

Kiểm tra trạng thái các container:
```bash
docker compose ps
```

Dừng và dọn dẹp hệ thống:
```bash
docker compose down
```
