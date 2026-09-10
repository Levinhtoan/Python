import pytest
from booking_app.schemas.booking import BookingCreate, BookingUpdate, BookingStatus
from booking_app.services.booking_service import BookingService

def test_postgres_repo_create_and_get(test_postgres_repo):
    """Kiểm tra tạo lịch hẹn và lấy danh sách qua Postgres repository."""
    booking_in = BookingCreate(
        customer="Nguyễn Văn A",
        service="Tư vấn sức khỏe",
        time="2026-09-15 10:00",
        notes="Gặp trực tiếp",
    )
    created = test_postgres_repo.create(booking_in)
    assert created.id is not None
    assert created.customer == "Nguyễn Văn A"
    assert created.status == BookingStatus.CONFIRMED

    # Lấy lại theo ID
    fetched = test_postgres_repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.customer == "Nguyễn Văn A"

    # Lấy tất cả
    all_bookings = test_postgres_repo.get_all()
    assert len(all_bookings) == 1
    assert all_bookings[0].id == created.id

def test_postgres_repo_update_and_delete(test_postgres_repo):
    """Kiểm tra cập nhật trạng thái và xóa lịch hẹn."""
    booking_in = BookingCreate(
        customer="Trần Thị B",
        service="Khám tổng quát",
        time="2026-09-20 09:00",
    )
    created = test_postgres_repo.create(booking_in)

    # Cập nhật trạng thái
    update_data = BookingUpdate(status=BookingStatus.CANCELLED)
    updated = test_postgres_repo.update(created.id, update_data)
    assert updated is not None
    assert updated.status == BookingStatus.CANCELLED

    # Xóa
    deleted = test_postgres_repo.delete(created.id)
    assert deleted is True

    # Kiểm tra không còn tồn tại
    assert test_postgres_repo.get_by_id(created.id) is None

def test_booking_service_with_postgres_repo(test_postgres_repo):
    """Kiểm tra BookingService hoạt động hoàn hảo với Postgres repository."""
    service = BookingService(repository=test_postgres_repo)

    booking_in = BookingCreate(
        customer="Lê Văn C",
        service="Cắt tóc gội đầu",
        time="2026-09-12 15:00",
    )
    created = service.create_booking(booking_in)
    assert created.customer == "Lê Văn C"

    cancelled = service.cancel_booking(created.id)
    assert cancelled.status == BookingStatus.CANCELLED
