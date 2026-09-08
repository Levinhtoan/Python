import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("🚀 Đang kiểm tra API trực tiếp...")

    # 1. Gọi GET /
    res = requests.get(f"{BASE_URL}/")
    print(f"\n1. GET / -> Status: {res.status_code}")
    print("   Response:", res.json())

    # 2. Gọi POST /api/v1/bookings (Tạo lịch hẹn mới)
    new_data = {
        "customer": "Hoàng Minh C",
        "service": "Tư vấn dinh dưỡng",
        "time": "2026-09-12 10:00",
        "notes": "Buổi đầu tiên"
    }
    res = requests.post(f"{BASE_URL}/api/v1/bookings", json=new_data)
    print(f"\n2. POST /api/v1/bookings -> Status: {res.status_code}")
    created_booking = res.json()
    print("   Created:", created_booking)
    booking_id = created_booking["id"]

    # 3. Gọi GET /api/v1/bookings (Xem danh sách)
    res = requests.get(f"{BASE_URL}/api/v1/bookings")
    print(f"\n3. GET /api/v1/bookings -> Tổng số lịch hẹn: {len(res.json())}")

    # 4. Gọi PUT /api/v1/bookings/{id}/cancel (Hủy lịch)
    res = requests.put(f"{BASE_URL}/api/v1/bookings/{booking_id}/cancel")
    print(f"\n4. PUT /api/v1/bookings/{booking_id}/cancel -> Status: {res.status_code}")
    print("   Updated Status:", res.json()["status"])

    print("\n✅ Toàn bộ kiểm thử API trực tiếp thành công!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Lỗi: Server API chưa được bật!")
        print("👉 Hãy chạy lệnh 'python run_api.py' ở một terminal trước, sau đó chạy lại script này.")
