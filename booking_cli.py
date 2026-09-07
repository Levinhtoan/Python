import json
import os
from datetime import datetime

DATA_FILE = "bookings.json"

def load_bookings():
    """Tải danh sách lịch hẹn từ file JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi khi đọc file dữ liệu: {e}")
        return []

def save_bookings(bookings):
    """Lưu danh sách lịch hẹn vào file JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

def add_booking():
    """Thêm một lịch hẹn mới."""
    print("\n--- ➕ THÊM LỊCH HẸN MỚI ---")
    customer = input("Tên khách hàng: ").strip()
    if not customer:
        print("❌ Tên khách hàng không được để trống!")
        return

    service = input("Tên dịch vụ (VD: Cắt tóc, Tư vấn, Khám bệnh): ").strip()
    time_str = input("Thời gian hẹn (VD: 2026-09-10 14:30): ").strip()
    notes = input("Ghi chú thêm (nếu có): ").strip()

    bookings = load_bookings()
    new_id = (bookings[-1]["id"] + 1) if bookings else 1

    new_booking = {
        "id": new_id,
        "customer": customer,
        "service": service,
        "time": time_str,
        "notes": notes,
        "status": "CONFIRMED",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    bookings.append(new_booking)
    save_bookings(bookings)
    print(f"✅ Đã thêm lịch hẹn thành công cho khách [{customer}] (Mã: {new_id})\n")

def list_bookings():
    """Xem toàn bộ danh sách lịch hẹn."""
    bookings = load_bookings()
    if not bookings:
        print("\n📭 Hiện chưa có lịch hẹn nào được ghi nhận.\n")
        return

    print("\n" + "=" * 75)
    print(f"{'MÃ':<5} | {'KHÁCH HÀNG':<20} | {'DỊCH VỤ':<18} | {'THỜI GIAN':<16} | {'TRẠNG THÁI'}")
    print("-" * 75)
    for b in bookings:
        print(f"{b['id']:<5} | {b['customer']:<20} | {b['service']:<18} | {b['time']:<16} | {b['status']}")
    print("=" * 75 + "\n")

def cancel_booking():
    """Hủy một lịch hẹn theo ID."""
    bookings = load_bookings()
    if not bookings:
        print("\n📭 Danh sách lịch hẹn rỗng.\n")
        return

    list_bookings()
    try:
        booking_id = int(input("Nhập mã (ID) lịch hẹn muốn hủy: ").strip())
    except ValueError:
        print("❌ ID phải là số nguyên!")
        return

    found = False
    for b in bookings:
        if b["id"] == booking_id:
            b["status"] = "CANCELLED"
            found = True
            break

    if found:
        save_bookings(bookings)
        print(f"✅ Đã hủy lịch hẹn mã [{booking_id}] thành công.\n")
    else:
        print(f"❌ Không tìm thấy lịch hẹn có mã [{booking_id}].\n")

def main():
    while True:
        print("========================================")
        print("📅 HỆ THỐNG QUẢN LÝ ĐẶT LỊCH (BOOKING)")
        print("========================================")
        print("1. Xem danh sách lịch hẹn")
        print("2. Đặt lịch hẹn mới")
        print("3. Hủy lịch hẹn")
        print("4. Thoát chương trình")
        print("========================================")
        choice = input("👉 Lựa chọn của bạn (1-4): ").strip()

        if choice == "1":
            list_bookings()
        elif choice == "2":
            add_booking()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            print("\n👋 Cảm ơn bạn đã sử dụng chương trình! Tạm biệt.")
            break
        else:
            print("\n❌ Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 4.\n")

if __name__ == "__main__":
    main()
