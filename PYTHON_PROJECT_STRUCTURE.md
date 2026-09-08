# Hướng Dẫn Cấu Trúc Thư Mục Chuẩn Cho Dự Án Python Thực Tế (Production-Ready)

Tài liệu này cung cấp các mô hình cấu trúc thư mục (Project Directory Layout) chuẩn quốc tế, đáp ứng các tiêu chuẩn PEP và Best Practices của cộng đồng Python hiện đại (sử dụng `src-layout`, Clean Architecture, quản lý package hiện đại).

---

## 1. Mô Hình Chuẩn Tổng Quát (Standard `src-layout`)

Mô hình **`src-layout`** được khuyến nghị bởi Python Packaging Authority (PyPA) vì giúp tránh lỗi import nhầm file local khi chạy test và đảm bảo code chạy đúng như khi được đóng gói (package/install).

```text
my_awesome_project/
│
├── .github/                      # Cấu hình CI/CD (GitHub Actions)
│   └── workflows/
│       ├── lint.yml              # Tự động kiểm tra định dạng code (Ruff, Flake8, Mypy)
│       └── tests.yml             # Tự động chạy Unit Test
│
├── .vscode/                      # Cấu hình IDE (khuyến nghị cho team)
│   ├── settings.json
│   └── launch.json
│
├── docs/                         # Tài liệu dự án (MkDocs, Sphinx, kiến trúc)
│   ├── index.md
│   └── architecture.md
│
├── requirements/                 # Quản lý dependencies theo từng môi trường
│   ├── base.txt                  # Các thư viện chung bắt buộc
│   ├── dev.txt                   # Thư viện cho môi trường lập trình (pytest, black, ruff)
│   └── prod.txt                  # Thư viện riêng cho production (gunicorn, sentry)
│
├── scripts/                      # Các script tiện ích (seed database, backup, migration)
│   └── setup_dev_data.py
│
├── src/                          # Mã nguồn chính của dự án (Source Code)
│   └── my_project/               # Tên package chính (dùng chữ thường + gạch dưới)
│       ├── __init__.py           # Đánh dấu thư mục là một Python package
│       ├── py.typed              # Đánh dấu package hỗ trợ Type Hints (PEP 561)
│       ├── main.py               # Entrypoint khi chạy ứng dụng
│       │
│       ├── core/                 # Cấu hình trung tâm, hằng số, bảo mật
│       │   ├── __init__.py
│       │   ├── config.py         # Đọc biến môi trường (.env), settings
│       │   ├── security.py       # Hash mật khẩu, JWT tokens
│       │   └── logging.py        # Cấu hình ghi log tập trung
│       │
│       ├── models/               # Định nghĩa thực thể dữ liệu (ORM: SQLAlchemy, Django, Peewee)
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── booking.py
│       │
│       ├── utils/                # Các hàm tiện ích dùng chung
│       │   ├── __init__.py
│       │   ├── date_helper.py
│       │   └── validators.py
│       │
│       └── ...
│
├── tests/                        # Toàn bộ test suite (tách biệt hoàn toàn khỏi src)
│   ├── conftest.py               # Fixtures dùng chung cho pytest
│   ├── unit/                     # Kiểm thử đơn vị
│   │   ├── test_user.py
│   │   └── test_booking.py
│   └── integration/              # Kiểm thử tích hợp (test gọi DB, API thật)
│       └── test_api.py
│
├── .env.example                  # Template biến môi trường (KHÔNG commit file .env thật)
├── .gitignore                    # Bỏ qua venv, cache, bytecode, file secret
├── .dockerignore                 # Bỏ qua file rác khi build Docker image
├── Dockerfile                    # Containerization cho ứng dụng
├── docker-compose.yml            # Khởi chạy ứng dụng + Database + Redis
├── pyproject.toml                # Cấu hình chuẩn hiện đại (Poetry, Flit, Ruff, Black, pytest)
├── README.md                     # Hướng dẫn cài đặt, chạy dự án
└── LICENSE                       # Giấy phép mã nguồn
```

---

## 2. Các Mô Hình Cấu Trúc Theo Từng Loại Dự Án Thực Tế

### Mẫu A: Dự án Web Backend / REST API (FastAPI, Flask) - Clean/Layered Architecture

Mô hình này phân tách ranh giới rõ ràng giữa các tầng: Routing -> Business Logic -> Data Access.

```text
fastapi_backend/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py                   # Khởi tạo FastAPI app, middlewares, CORS, router
│       │
│       ├── api/                      # Giao tiếp HTTP / Controllers
│       │   ├── __init__.py
│       │   ├── deps.py               # Dependency Injection (lấy DB session, current user)
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── router.py         # Gom tất cả router v1
│       │       └── endpoints/
│       │           ├── auth.py
│       │           ├── users.py
│       │           └── bookings.py
│       │
│       ├── core/                     # Cốt lõi hệ thống
│       │   ├── config.py             # Pydantic BaseSettings đọc file .env
│       │   ├── database.py           # Kết nối Database engine, SessionLocal
│       │   ├── exceptions.py         # Custom Exceptions toàn hệ thống
│       │   └── security.py           # Hash password, mã hóa Token
│       │
│       ├── schemas/                  # Pydantic Models (Validation Request/Response)
│       │   ├── user.py               # UserCreate, UserResponse, UserUpdate
│       │   └── booking.py
│       │
│       ├── models/                   # Database ORM Models (SQLAlchemy / SQLModel)
│       │   ├── user.py
│       │   └── booking.py
│       │
│       ├── repositories/             # Tầng truy vấn CSDL (CRUD operations)
│       │   ├── base.py
│       │   ├── user_repo.py
│       │   └── booking_repo.py
│       │
│       └── services/                 # Tầng xử lý logic nghiệp vụ (Business Logic)
│           ├── auth_service.py
│           ├── user_service.py
│           └── booking_service.py
│
├── alembic/                          # Database Migrations (nếu dùng SQLAlchemy + Alembic)
│   ├── versions/
│   └── env.py
├── alembic.ini
├── tests/
├── .env.example
├── pyproject.toml
└── Dockerfile
```

---

### Mẫu B: Dự án Ứng Dụng Dòng Lệnh (CLI Tool) hoặc Thư Viện (Library/Package)

Phù hợp khi bạn viết tool dùng `argparse`, `click`, `typer` hoặc phát hành thư viện lên PyPI.

```text
my_cli_tool/
├── src/
│   └── my_tool/
│       ├── __init__.py
│       ├── __main__.py               # Cho phép chạy: `python -m my_tool`
│       ├── cli.py                    # Định nghĩa các command, options, arguments
│       ├── core.py                   # Logic xử lý chính
│       └── formatter.py              # Định dạng output màn hình (Rich, Colorama)
│
├── tests/
│   ├── test_cli.py
│   └── test_core.py
│
├── pyproject.toml                    # Khai báo [project.scripts] để cài đặt lệnh terminal
└── README.md
```

---

### Mẫu C: Dự án Khoa Học Dữ Liệu / Trí Tuệ Nhân Tạo (Data Science / Machine Learning)

Mô hình theo chuẩn **Cookiecutter Data Science** phổ biến trong ngành:

```text
ml_project/
├── data/                             # Dữ liệu (KHÔNG đưa lên Git trừ file sample)
│   ├── raw/                          # Dữ liệu gốc bất biến
│   ├── interim/                      # Dữ liệu đang xử lý trung gian
│   └── processed/                    # Dữ liệu sạch sẵn sàng để train model
│
├── notebooks/                        # Jupyter Notebooks để khám phá EDA, thử nghiệm
│   ├── 1.0-data-exploration.ipynb
│   └── 2.0-model-prototyping.ipynb
│
├── models/                           # Model đã train (weights, .pkl, .onnx)
│
├── src/
│   └── ml_project/
│       ├── __init__.py
│       ├── dataset.py                # Script tải, parse và transform dữ liệu
│       ├── features.py               # Feature Engineering
│       ├── train.py                  # Script huấn luyện mô hình
│       ├── predict.py                # Script suy luận (Inference)
│       └── evaluate.py               # Đánh giá độ chính xác
│
├── configs/                          # Hyperparameters và cấu hình training (YAML / JSON)
│   └── train_config.yaml
│
├── pyproject.toml
└── requirements.txt
```

---

## 3. Ý Nghĩa & Vai Trò Của Các File Quan Trọng

| File / Folder | Mục Đích & Vai Trò |
| :--- | :--- |
| `src/` | Chứa code chính. Giúp cách ly hoàn toàn môi trường chạy và thư mục test. |
| `__init__.py` | Đánh dấu thư mục là một Python package. Có thể để trống hoặc export các class/function chính (`__all__`). |
| `pyproject.toml` | **Tiêu chuẩn cấu hình hiện đại (PEP 518 & 621)**. Gom cấu hình build, dependencies, linter (Ruff), formatter (Black), test runner (pytest) vào một file duy nhất. |
| `.env.example` | File mẫu chứa danh sách các key cấu hình (như `DATABASE_URL`, `SECRET_KEY`) không kèm thông tin nhạy cảm. |
| `.env` | File chứa giá trị biến môi trường thật trên máy bạn (Phải nằm trong `.gitignore`, không bao giờ commit). |
| `conftest.py` | Nơi chứa các `pytest fixture` (khởi tạo database ảo, mock API client) tái sử dụng cho toàn bộ test. |
| `.gitignore` | Bỏ qua các file không cần thiết: `__pycache__/`, `*.pyc`, `.env`, `venv/`, `.pytest_cache/`. |
| `Dockerfile` | Định nghĩa môi trường chạy ứng dụng nhất quán giữa local và production. |

---

## 4. Các Nguyên Tắc Vàng (Best Practices) Khi Làm Dự Án Python Thực Tế

### 1. Luôn sử dụng Môi trường ảo (Virtual Environment)
Không bao giờ cài thư viện trực tiếp vào Global Python của hệ điều hành.
```bash
# Khởi tạo môi trường ảo
python -m venv venv

# Kích hoạt trên Windows
.\venv\Scripts\activate

# Kích hoạt trên macOS/Linux
source venv/bin/activate
```
*(Gợi ý hiện đại: Sử dụng `uv` hoặc `poetry` để quản lý môi trường và cài đặt dependencies với tốc độ cực nhanh).*

### 2. Sử dụng Absolute Import thay vì Relative Import lộn xộn
- **Khuyên dùng:**
  ```python
  from src.my_project.core.config import settings
  from src.my_project.services.user_service import UserService
  ```
- **Hạn chế:**
  ```python
  from ...core.config import settings  # Rất khó bảo trì khi đổi cấu trúc thư mục
  ```

### 3. Tách biệt Cấu hình theo nguyên lý 12-Factor App
- Không hardcode chuỗi kết nối Database, API Key hoặc Secret Token vào code.
- Sử dụng thư viện `python-dotenv` hoặc `pydantic-settings` để đọc từ biến môi trường.

### 4. Tự động hóa kiểm tra Code Quality
Nên tích hợp các công cụ sau vào quy trình làm việc (khai báo trong `pyproject.toml`):
- **Formatter & Linter:** `ruff` (Cực nhanh, thay thế Black + Flake8 + isort).
- **Type Checker:** `mypy` (Kiểm tra kiểu dữ liệu tĩnh).
- **Test Runner:** `pytest` (Khung kiểm thử chuẩn).
- **Pre-commit hook:** Tự động format và kiểm tra lỗi trước khi `git commit`.

---

## 5. Mẫu File `pyproject.toml` Hiện Đại Tham Khảo

```toml
[project]
name = "my-awesome-project"
version = "0.1.0"
description = "Hệ thống quản lý đặt phòng và lịch hẹn"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.28.0",
    "sqlalchemy>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.3.0",
    "mypy>=1.8.0",
    "pre-commit>=3.6.0",
]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "W", "UP"]

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --cov=src"
testpaths = ["tests"]
```
