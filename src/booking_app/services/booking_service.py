from typing import List, Optional
from booking_app.repositories.base import BaseBookingRepository
from booking_app.schemas.booking import (
    BookingCreate,
    BookingResponse,
    BookingUpdate,
    BookingStatus,
)
from booking_app.core.exceptions import (
    BookingNotFoundException,
    BookingValidationException,
)

class BookingService:
    """Tầng xử lý logic nghiệp vụ (Business Logic Layer) của hệ thống Booking."""

    def __init__(self, repository: BaseBookingRepository):
        self.repository = repository

    def list_all_bookings(self) -> List[BookingResponse]:
        """Lấy tất cả danh sách lịch hẹn."""
        return self.repository.get_all()

    def get_booking(self, booking_id: int) -> BookingResponse:
        """Lấy chi tiết một lịch hẹn theo ID."""
        booking = self.repository.get_by_id(booking_id)
        if not booking:
            raise BookingNotFoundException(booking_id)
        return booking

    def create_booking(self, booking_in: BookingCreate) -> BookingResponse:
        """Tạo mới một lịch hẹn với các kiểm tra hợp lệ nghiệp vụ."""
        if not booking_in.customer.strip():
            raise BookingValidationException("Tên khách hàng không được để trống!")
        if not booking_in.service.strip():
            raise BookingValidationException("Tên dịch vụ không được để trống!")
        return self.repository.create(booking_in)

    def cancel_booking(self, booking_id: int) -> BookingResponse:
        """Hủy lịch hẹn đã đặt."""
        booking = self.get_booking(booking_id)
        if booking.status == BookingStatus.CANCELLED:
            return booking  # Đã hủy từ trước

        update_dto = BookingUpdate(status=BookingStatus.CANCELLED)
        updated = self.repository.update(booking_id, update_dto)
        if not updated:
            raise BookingNotFoundException(booking_id)
        return updated

    def delete_booking(self, booking_id: int) -> bool:
        """Xóa vĩnh viễn lịch hẹn khỏi hệ thống."""
        self.get_booking(booking_id)  # Kiểm tra tồn tại
        return self.repository.delete(booking_id)
