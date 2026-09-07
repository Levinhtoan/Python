# 🐍 Python Learning & Booking API Project

Dự án học lập trình Python từ cơ bản đến nâng cao và xây dựng REST API bằng FastAPI.

## 📂 Cấu Trúc Thư Mục

- `Tai_Lieu_Hoc_Python.md`: Tài liệu hướng dẫn học Python toàn diện (Cơ bản -> Nâng cao).
- `booking_cli.py`: Ứng dụng Quản lý đặt lịch hẹn dạng dòng lệnh (CLI Console).
- `main.py`: REST API Quản lý đặt lịch xây dựng bằng **FastAPI** và **Pydantic**.
- `test_api.py`: Script kiểm thử API bằng thư viện `requests`.
- `requirements.txt`: Danh sách các thư viện cần thiết.

## 🚀 Hướng Dẫn Cài Đặt & Chạy

### 1. Tạo môi trường ảo & cài đặt thư viện
```bash
python -m venv venv
# Kích hoạt trên Windows:
.\venv\Scripts\activate

# Cài đặt thư viện:
pip install -r requirements.txt
```

### 2. Chạy API FastAPI
```bash
python main.py
```
Truy cập tài liệu API tương tác tại: **http://127.0.0.1:8000/docs**

### 3. Chạy ứng dụng CLI
```bash
python booking_cli.py
```
