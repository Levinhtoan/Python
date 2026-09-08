# 📅 Booking & Scheduling Management System

Dự án mẫu quản lý đặt lịch hẹn thực tế được xây dựng theo kiến trúc **Clean Architecture** và chuẩn **`src-layout`** chuẩn mực của Python Packaging (tham khảo [PYTHON_PROJECT_STRUCTURE.md](file:///e:/Booking-SchedulingManagement/PYTHON_PROJECT_STRUCTURE.md)).

---

## 🌟 Tính Năng Chính

- **RESTful API (FastAPI)**: Đầy đủ CRUD đặt lịch, hủy lịch, xem danh sách và Swagger UI interactive docs (`/docs`).
- **Giao diện CLI**: Menu console trực quan tương tác trực tiếp với tầng Service.
- **Phân tầng Clean Architecture**:
  - `schemas`: DTO / Data Validation với Pydantic v2.
  - `repositories`: Trừu tượng hóa việc lưu trữ (JSON file storage & Base interface).
  - `services`: Xử lý toàn bộ logic nghiệp vụ (Business logic độc lập).
  - `api`: Fast, clean routing và dependency injection.
- **Kiểm thử tự động (Pytest)**: Unit tests cho tầng service và Integration tests cho API endpoints.
- **Docker & CI/CD**: Hỗ trợ Dockerfile, Docker Compose và GitHub Actions Workflow.

---

## 📂 Cấu Trúc Dự Án

```text
Booking-SchedulingManagement/
├── .github/workflows/tests.yml   # CI/CD Tự động chạy Unit Test
├── data/bookings.json            # File lưu trữ dữ liệu
├── requirements/
│   ├── base.txt                  # Thư viện runtime chính
│   └── dev.txt                   # Thư viện cho môi trường dev & test
├── src/
│   └── booking_app/
│       ├── api/                  # Tầng giao tiếp HTTP (Routers, Endpoints, Deps)
│       ├── core/                 # Cấu hình hệ thống (Settings, Custom Exceptions)
│       ├── models/ & schemas/    # Pydantic Schemas & DTOs
│       ├── repositories/         # Tầng lưu trữ dữ liệu (Repository Pattern)
│       ├── services/             # Tầng nghiệp vụ cốt lõi (Business Logic)
│       ├── main.py               # Entrypoint FastAPI Server
│       └── cli.py                # Entrypoint Giao diện dòng lệnh
├── tests/
│   ├── conftest.py               # Fixtures dùng chung cho pytest
│   ├── unit/                     # Unit test cho Service Layer
│   └── integration/              # Integration test cho API Routes
├── .env.example                  # Template biến môi trường
├── Dockerfile & docker-compose.yml
├── pyproject.toml                # Cấu hình dự án & Pytest
├── run_api.py                    # Script chạy nhanh FastAPI server
└── run_cli.py                    # Script chạy nhanh CLI console
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

### 3. Chạy API Server
```bash
python run_api.py
```
- Truy cập Swagger API Docs tại: **http://127.0.0.1:8000/docs**
- Trang chủ API: **http://127.0.0.1:8000/**

### 4. Chạy Giao diện CLI Console
```bash
python run_cli.py
```

### 5. Chạy Automated Tests (Pytest)
```bash
pytest
```

### 6. Khởi chạy bằng Docker Compose
```bash
docker-compose up -d --build
```
