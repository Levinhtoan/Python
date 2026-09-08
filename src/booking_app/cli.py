import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from pydantic import ValidationError
from booking_app.api.deps import get_booking_service
from booking_app.schemas.booking import BookingCreate
from booking_app.core.exceptions import (
    BookingNotFoundException,
    BookingValidationException,
)

def print_header(title: str):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

def handle_list_bookings(service):
    bookings = service.list_all_bookings()
    if not bookings:
        print("\n📭 Hiện chưa có lịch hẹn nào.")
        return

    print("\n" + "-" * 85)
    print(f"{'MÃ':<5} | {'KHÁCH HÀNG':<22} | {'DỊCH VỤ':<20} | {'THỜI GIAN':<18} | {'TRẠNG THÁI'}")
    print("-" * 85)
    for b in bookings:
        print(f"{b.id:<5} | {b.customer:<22} | {b.service:<20} | {b.time:<18} | {b.status.value}")
    print("-" * 85)

def handle_create_booking(service):
    print("\n--- ➕ ĐẶT LỊCH HẸN MỚI ---")
    customer = input("Tên khách hàng: ").strip()
    service_name = input("Tên dịch vụ (VD: Khám bệnh, Cắt tóc, Tư vấn): ").strip()
    time_str = input("Thời gian hẹn (VD: 2026-09-15 10:00): ").strip()
    notes = input("Ghi chú thêm (tùy chọn): ").strip() or None

    try:
        booking_in = BookingCreate(
            customer=customer,
            service=service_name,
            time=time_str,
            notes=notes,
        )
        created = service.create_booking(booking_in)
        print(f"\n✅ Đã tạo lịch hẹn thành công! Mã số: [#{created.id}]")
    except ValidationError as e:
        print("\n❌ Dữ liệu không hợp lệ:")
        for err in e.errors():
            field = " -> ".join(str(loc) for loc in err["loc"])
            print(f"   • Trường '{field}': {err['msg']}")
    except BookingValidationException as e:
        print(f"\n❌ Lỗi nghiệp vụ: {e}")
    except Exception as e:
        print(f"\n❌ Đã xảy ra lỗi: {e}")

def handle_cancel_booking(service):
    print("\n--- ❌ HỦY LỊCH HẸN ---")
    raw_id = input("Nhập mã (ID) lịch hẹn cần hủy: ").strip()
    if not raw_id.isdigit():
        print("❌ ID phải là số nguyên.")
        return

    try:
        updated = service.cancel_booking(int(raw_id))
        print(f"\n✅ Lịch hẹn [#{updated.id}] của [{updated.customer}] đã chuyển sang trạng thái CANCELLED.")
    except BookingNotFoundException as e:
        print(f"\n❌ {e}")

def handle_delete_booking(service):
    print("\n--- 🗑️ XÓA LỊCH HẸN ---")
    raw_id = input("Nhập mã (ID) lịch hẹn cần xóa: ").strip()
    if not raw_id.isdigit():
        print("❌ ID phải là số nguyên.")
        return

    try:
        service.delete_booking(int(raw_id))
        print(f"\n✅ Đã xóa thành công lịch hẹn mã [#{raw_id}].")
    except BookingNotFoundException as e:
        print(f"\n❌ {e}")

def main():
    service = get_booking_service()
    while True:
        print_header("📅 HỆ THỐNG QUẢN LÝ ĐẶT LỊCH HẸN (CLI)")
        print("1. Xem toàn bộ danh sách lịch hẹn")
        print("2. Đặt lịch hẹn mới")
        print("3. Hủy một lịch hẹn")
        print("4. Xóa vĩnh viễn lịch hẹn")
        print("5. Thoát")
        print("-" * 50)
        choice = input("👉 Chọn chức năng (1-5): ").strip()

        if choice == "1":
            handle_list_bookings(service)
        elif choice == "2":
            handle_create_booking(service)
        elif choice == "3":
            handle_cancel_booking(service)
        elif choice == "4":
            handle_delete_booking(service)
        elif choice == "5":
            print("\n👋 Cảm ơn bạn đã sử dụng hệ thống. Hẹn gặp lại!")
            sys.exit(0)
        else:
            print("\n⚠️ Lựa chọn không hợp lệ, vui lòng thử lại.")

if __name__ == "__main__":
    main()
