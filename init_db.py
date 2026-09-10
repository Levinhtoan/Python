import sys
import os

# Thêm src vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from booking_app.core.config import settings
from booking_app.db.session import init_db

def main():
    print("=" * 60)
    print("🚀 TIẾN HÀNH KHỞI TẠO BẢNG CƠ SỞ DỮ LIỆU POSTGRESQL / SQL")
    print("=" * 60)
    print(f"📌 Storage Mode : {settings.DB_TYPE}")
    print(f"📌 Database URL : {settings.sync_database_url}")
    print("-" * 60)
    try:
        init_db()
        print("✅ Khởi tạo các bảng database thành công! Bảng 'bookings' đã sẵn sàng.")
    except Exception as e:
        print(f"❌ Lỗi khi khởi tạo database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
