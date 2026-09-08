# 🧭 SƠ ĐỒ VÀ LUỒNG CHẠY HỆ THỐNG (EXECUTION FLOW)
**Dự Án: Booking & Scheduling Management System**

---

## 📑 MỤC LỤC
1. [Tổng Quan Kiến Trúc (Clean Architecture)](#1-tổng-quan-kiến-trúc-clean-architecture)
2. [Luồng Khởi Động Hệ Thống (Startup Lifecycle)](#2-luồng-khởi-động-hệ-thống-startup-lifecycle)
   - [2.1. Luồng chạy REST API Server (FastAPI)](#21-luồng-chạy-rest-api-server-fastapi)
   - [2.2. Luồng chạy Giao diện Dòng lệnh (CLI)](#22-luồng-chạy-giao-diện-dòng-lệnh-cli)
3. [Luồng Xử Lý Dữ Liệu & Request-Response (Request Lifecycle)](#3-luồng-xử-lý-dữ-liệu--request-response-request-lifecycle)
   - [3.1. Luồng Tạo mới Lịch hẹn (POST /api/v1/bookings)](#31-luồng-tạo-mới-lịch-hẹn-post-apiv1bookings)
   - [3.2. Luồng Xem danh sách & Chi tiết (GET)](#32-luồng-xem-danh-sách--chi-tiết-get)
   - [3.3. Luồng Hủy lịch hẹn (PUT /api/v1/bookings/{id}/cancel)](#33-luồng-hủy-lịch-hẹn-put-apiv1bookingsidcancel)
4. [Sơ Đồ Phụ Thuộc & Dependency Injection (DI Flow)](#4-sơ-đồ-phụ-thuộc--dependency-injection-di-flow)
5. [Cơ Chế Lưu Trữ Dữ Liệu (Data Persistence Flow)](#5-cơ-chế-lưu-trữ-dữ-liệu-data-persistence-flow)
6. [Luồng Kiểm Thử & Tự Động Hóa (Testing & CI/CD Flow)](#6-luồng-kiểm-thử--tự-động-hóa-testing--cicd-flow)
7. [Bản Đồ Điều Hướng File Trong Luồng Chạy](#7-bản-đồ-điều-hướng-file-trong-luồng-chạy)

---

## 1. Tổng Quan Kiến Trúc (Clean Architecture)

Hệ thống được thiết kế tách lớp độc lập theo nguyên lý **Inversion of Control (IoC)** và **Separation of Concerns**:

```mermaid
graph TD
    Client["🌐 Client (Web Browser / Postman / Swagger / Terminal)"]
    
    subgraph Presentation_Layer["1. Presentation Layer (Tầng Giao Diện / Giao Tiếp)"]
        API["FastAPI Routes (`src/booking_app/api/`)"]
        CLI["CLI Interface (`src/booking_app/cli.py`)"]
    end

    subgraph DI_Layer["Dependency Injection"]
        Deps["`src/booking_app/api/deps.py`"]
    end

    subgraph Business_Layer["2. Business Logic Layer (Tầng Nghiệp Vụ)"]
        Service["`BookingService` (`src/booking_app/services/booking_service.py`)"]
    end

    subgraph Data_Layer["3. Data Access Layer (Tầng Kho Lưu Trữ)"]
        RepoInterface["`BaseBookingRepository` (Interface trừu tượng)"]
        JSONRepo["`JSONBookingRepository` (Triển khai cụ thể)"]
    end

    subgraph Storage_Layer["4. Storage / Persistence"]
        JSONFile["File JSON (`data/bookings.json`)"]
    end

    subgraph Schema_Layer["Cross-Cutting: Schemas & Validation"]
        Schemas["Pydantic Models (`src/booking_app/schemas/booking.py`)"]
    end

    Client -->|HTTP Request| API
    Client -->|Terminal Input| CLI
    API --> Deps
    CLI --> Deps
    Deps -->|Inject Repository| Service
    Service -->|Gọi qua Interface| RepoInterface
    RepoInterface -.->|Triển khai thực tế| JSONRepo
    JSONRepo -->|Đọc / Ghi File| JSONFile
    
    Schemas -.->|Validate & Định kiểu| API
    Schemas -.->|Validate & Định kiểu| CLI
    Schemas -.->|Sử dụng DTOs| Service
    Schemas -.->|Chuyển đổi DTOs| JSONRepo
```

---

## 2. Luồng Khởi Động Hệ Thống (Startup Lifecycle)

### 2.1. Luồng chạy REST API Server (FastAPI)

Khi người dùng chạy lệnh:
```bash
python run_api.py
```

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng
    participant Run as run_api.py
    participant Config as core/config.py
    participant Main as booking_app/main.py
    participant Router as api/v1/router.py
    participant Uvicorn as Uvicorn ASGI Server

    User->>Run: Thực thi `python run_api.py`
    Run->>Config: Tải cấu hình `settings` (HOST, PORT, DATA_FILE_PATH)
    Run->>Uvicorn: Gọi `uvicorn.run("booking_app.main:app", host, port, reload=True)`
    Uvicorn->>Main: Import module và gọi `create_app()`
    Main->>Main: Cấu hình FastAPI instance, CORS Middleware, Swagger metadata
    Main->>Router: Nạp `api_router` với tiền tố `/api/v1`
    Router->>Router: Đăng ký router con `bookings.router` (tags=["Đặt lịch hẹn"])
    Main-->>Uvicorn: Trả về ASGI Application Object (`app`)
    Uvicorn-->>User: Lắng nghe kết nối tại `http://127.0.0.1:8000`
```

---

### 2.2. Luồng chạy Giao diện Dòng lệnh (CLI)

Khi người dùng chạy lệnh:
```bash
python run_cli.py
```

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng (Terminal)
    participant Run as run_cli.py
    participant CLI as booking_app/cli.py
    participant Deps as api/deps.py
    participant Service as booking_service.py

    User->>Run: Thực thi `python run_cli.py`
    Run->>CLI: Gọi hàm `main()`
    CLI->>Deps: Gọi `get_booking_service()`
    Deps->>Deps: Khởi tạo Repository Singleton (`JSONBookingRepository`)
    Deps->>Service: Inject Repository vào `BookingService(repository)`
    Deps-->>CLI: Trả về đối tượng `service`
    loop Menu Vòng lặp
        CLI->>User: Hiển thị bảng chọn (1. Xem, 2. Đặt lịch, 3. Hủy, 4. Xóa, 5. Thoát)
        User->>CLI: Nhập số lựa chọn & thông tin
        CLI->>Service: Gọi hàm nghiệp vụ tương ứng
        Service-->>CLI: Kết quả / Ngoại lệ (Exception)
        CLI-->>User: In kết quả định dạng bảng ra màn hình console
    end
```

---

## 3. Luồng Xử Lý Dữ Liệu & Request-Response (Request Lifecycle)

### 3.1. Luồng Tạo mới Lịch hẹn (`POST /api/v1/bookings`)

Đây là ví dụ luồng toàn diện đi qua toàn bộ các tầng:

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client / Swagger
    participant Endpoints as api/v1/endpoints/bookings.py
    participant Pydantic as schemas/booking.py
    participant Deps as api/deps.py
    participant Service as services/booking_service.py
    participant Repo as repositories/json_repository.py
    participant File as data/bookings.json

    Client->>Endpoints: POST /api/v1/bookings (JSON Payload)
    Note over Endpoints,Pydantic: Bước 1: Data Validation & Schema Parsing
    Endpoints->>Pydantic: Parse request body thành `BookingCreate`
    alt Dữ liệu không hợp lệ (Trống tên / sai kiểu)
        Pydantic-->>Client: 422 Unprocessable Entity (FastAPI tự động)
    end

    Note over Endpoints,Deps: Bước 2: Dependency Injection
    Endpoints->>Deps: Resolve dependency `get_booking_service`
    Deps-->>Endpoints: Cung cấp `BookingService` instance

    Note over Endpoints,Service: Bước 3: Business Logic
    Endpoints->>Service: Gọi `create_booking(booking_in)`
    Service->>Service: Kiểm tra logic (customer.strip(), service.strip())
    alt Lỗi nghiệp vụ
        Service-->>Endpoints: Ném `BookingValidationException`
        Endpoints-->>Client: HTTP 400 Bad Request
    end

    Note over Service,Repo: Bước 4: Data Persistence
    Service->>Repo: Gọi `repository.create(booking_in)`
    Repo->>File: Đọc danh sách hiện tại từ `data/bookings.json`
    File-->>Repo: List[dict]
    Repo->>Repo: Tính toán `id = max_id + 1`, gán trạng thái `CONFIRMED`, `created_at`
    Repo->>File: Ghi đè file JSON với mảng đã thêm bản ghi mới
    Repo-->>Service: Trả về `BookingResponse` (Pydantic model)
    Service-->>Endpoints: Trả về `BookingResponse`
    Endpoints-->>Client: HTTP 201 Created + JSON Response
```

---

### 3.2. Luồng Xem danh sách & Chi tiết (GET)

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client
    participant Endpoints as api/v1/endpoints/bookings.py
    participant Service as services/booking_service.py
    participant Repo as repositories/json_repository.py
    participant File as data/bookings.json

    Client->>Endpoints: GET /api/v1/bookings/{id}
    Endpoints->>Service: get_booking(id)
    Service->>Repo: get_by_id(id)
    Repo->>File: Đọc file `data/bookings.json`
    File-->>Repo: Dữ liệu thô JSON
    alt Tìm thấy ID
        Repo-->>Service: Đối tượng `BookingResponse`
        Service-->>Endpoints: `BookingResponse`
        Endpoints-->>Client: HTTP 200 OK + JSON
    else Không tìm thấy
        Repo-->>Service: Trả về `None`
        Service-->>Endpoints: Ném `BookingNotFoundException(id)`
        Endpoints-->>Client: HTTP 404 Not Found `{"detail": "Không tìm thấy lịch hẹn mã #..."}`
    end
```

---

### 3.3. Luồng Hủy lịch hẹn (`PUT /api/v1/bookings/{id}/cancel`)

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client
    participant Endpoints as api/v1/endpoints/bookings.py
    participant Service as services/booking_service.py
    participant Repo as repositories/json_repository.py
    participant File as data/bookings.json

    Client->>Endpoints: PUT /api/v1/bookings/{id}/cancel
    Endpoints->>Service: cancel_booking(id)
    Service->>Service: get_booking(id) để kiểm tra tồn tại
    alt Đã hủy từ trước (status == CANCELLED)
        Service-->>Endpoints: Trả về trạng thái hiện tại (Idempotent)
    else Chưa hủy
        Service->>Repo: update(id, BookingUpdate(status="CANCELLED"))
        Repo->>File: Đọc file, cập nhật field `status = "CANCELLED"`, lưu file
        Repo-->>Service: Trả về `BookingResponse` đã update
        Service-->>Endpoints: Trả về `BookingResponse`
    end
    Endpoints-->>Client: HTTP 200 OK + JSON
```

---

## 4. Sơ Đồ Phụ Thuộc & Dependency Injection (DI Flow)

File `src/booking_app/api/deps.py` đóng vai trò là **Composition Root** (nơi liên kết các thành phần phụ thuộc với nhau):

```text
┌────────────────────────────────────────────────────────┐
│                   api/deps.py                          │
│                                                        │
│  @lru_cache()                                          │
│  def get_repository() -> JSONBookingRepository:        │
│       return JSONBookingRepository("data/bookings.json")│
│                                                        │
│  def get_booking_service() -> BookingService:          │
│       repo = get_repository()                          │
│       return BookingService(repository=repo)           │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
┌─────────────────────────┐ ┌─────────────────────────┐
│     FastAPI Endpoints   │ │       CLI Console       │
│ Depends(get_booking_srv)│ │ get_booking_service()   │
└─────────────────────────┘ └─────────────────────────┘
```

> **Lợi ích kiến trúc:**
> * Khi cần chuyển từ lưu file JSON sang cơ sở dữ liệu **PostgreSQL / MySQL / MongoDB**, chỉ cần viết `SQLBookingRepository(BaseBookingRepository)` và thay đổi ở `deps.py`.
> * Toàn bộ code ở tầng **API**, **CLI** và **Service** hoàn toàn giữ nguyên 100% không cần sửa đổi!

---

## 5. Cơ Chế Lưu Trữ Dữ Liệu (Data Persistence Flow)

Cơ chế quản lý file `data/bookings.json`:

1. **Khởi tạo tự động**: Khi `JSONBookingRepository` được tạo, hàm `_ensure_file_exists()` tự động tạo thư mục `data/` và file rỗng `[]` nếu chưa tồn tại.
2. **Đọc dữ liệu (`_read_data`)**: Mở file với mã hóa `utf-8`, dùng `json.load()` để chuyển thành danh sách từ điển Python.
3. **Ghi dữ liệu (`_write_data`)**: Dùng `json.dump(..., ensure_ascii=False, indent=2)` để đảm bảo lưu đúng tiếng Việt có dấu và định dạng đẹp mắt.
4. **Tự tăng ID (Auto-increment)**: `new_id = raw_list[-1]["id"] + 1 if raw_list else 1`.

---

## 6. Luồng Kiểm Thử & Tự Động Hóa (Testing & CI/CD Flow)

```mermaid
graph LR
    subgraph Local_Developer["Máy Lập Trình Viên"]
        PytestCommand["Chạy `pytest`"]
        UnitTests["Unit Tests (`tests/unit/`)<br>Mock Repository - Test logic Service"]
        IntegrationTests["Integration Tests (`tests/integration/`)<br>TestClient FastAPI - Test Endpoint"]
    end

    subgraph GitHub_Actions["GitHub Actions Workflow (`.github/workflows/tests.yml`)"]
        GitPush["git push / PR"]
        SetupPy["Cài đặt Python 3.10, 3.11, 3.12"]
        InstallReq["pip install -r requirements/dev.txt"]
        RunPytest["Chạy pytest tự động"]
    end

    PytestCommand --> UnitTests
    PytestCommand --> IntegrationTests
    GitPush --> SetupPy --> InstallReq --> RunPytest
```

---

## 7. Bản Đồ Điều Hướng File Trong Luồng Chạy

| File | Vai trò trong luồng | Mô tả nhiệm vụ |
| :--- | :--- | :--- |
| `run_api.py` | **Entrypoint Web** | Khởi chạy Uvicorn Server và FastAPI |
| `run_cli.py` | **Entrypoint CLI** | Khởi chạy giao diện console dòng lệnh |
| `src/booking_app/main.py` | **App Factory** | Khởi tạo app FastAPI, nạp CORS, Swagger docs và router |
| `src/booking_app/core/config.py` | **Config Layer** | Đọc biến môi trường (Host, Port, File path) |
| `src/booking_app/core/exceptions.py` | **Exception Layer**| Định nghĩa các ngoại lệ nghiệp vụ (NotFound, Validation) |
| `src/booking_app/schemas/booking.py`| **DTO / Schemas** | Xác thực dữ liệu đầu vào / đầu ra bằng Pydantic v2 |
| `src/booking_app/api/deps.py` | **Dependency Root** | Khởi tạo và phân phối Service & Repository |
| `src/booking_app/api/v1/endpoints/bookings.py` | **HTTP Controller** | Tiếp nhận HTTP Request, gọi Service, trả về HTTP Response |
| `src/booking_app/services/booking_service.py` | **Business Logic** | Xử lý quy tắc nghiệp vụ đặt lịch, hủy lịch |
| `src/booking_app/repositories/base.py` | **Abstract Interface**| Quy định các hàm chuẩn CRUD của Repository |
| `src/booking_app/repositories/json_repository.py` | **Data Access** | Đọc và ghi dữ liệu trực tiếp vào `data/bookings.json` |
| `data/bookings.json` | **Database File** | Nơi lưu trữ thực tế của các bản ghi lịch hẹn |
