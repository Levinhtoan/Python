import pytest
from booking_app.schemas.booking import BookingCreate, BookingStatus
from booking_app.core.exceptions import (
    BookingNotFoundException,
    BookingValidationException,
)

def test_create_booking_success(test_service):
    payload = BookingCreate(
        customer="Nguyễn Văn A",
        service="Cắt tóc tạo kiểu",
        time="2026-09-15 14:00",
        notes="Gội đầu thảo dược"
    )
    result = test_service.create_booking(payload)

    assert result.id == 1
    assert result.customer == "Nguyễn Văn A"
    assert result.service == "Cắt tóc tạo kiểu"
    assert result.status == BookingStatus.CONFIRMED

def test_create_booking_empty_name_raises_error(test_service):
    payload = BookingCreate(
        customer="   ",
        service="Khám bệnh",
        time="2026-09-15 14:00"
    )
    with pytest.raises(BookingValidationException):
        test_service.create_booking(payload)

def test_get_booking_by_id(test_service):
    payload = BookingCreate(
        customer="Trần Thị B",
        service="Spa chăm sóc da",
        time="2026-09-16 10:00"
    )
    created = test_service.create_booking(payload)
    fetched = test_service.get_booking(created.id)

    assert fetched.id == created.id
    assert fetched.customer == "Trần Thị B"

def test_get_nonexistent_booking_raises_not_found(test_service):
    with pytest.raises(BookingNotFoundException):
        test_service.get_booking(999)

def test_cancel_booking(test_service):
    payload = BookingCreate(
        customer="Lê Văn C",
        service="Tư vấn",
        time="2026-09-17 15:00"
    )
    created = test_service.create_booking(payload)
    cancelled = test_service.cancel_booking(created.id)

    assert cancelled.status == BookingStatus.CANCELLED
