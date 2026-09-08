class BookingAppException(Exception):
    """Lớp ngoại lệ cơ sở cho toàn bộ ứng dụng."""
    pass

class BookingNotFoundException(BookingAppException):
    """Ngoại lệ khi không tìm thấy lịch hẹn."""
    def __init__(self, booking_id: int):
        self.booking_id = booking_id
        super().__init__(f"Không tìm thấy lịch hẹn với mã ID: {booking_id}")

class BookingValidationException(BookingAppException):
    """Ngoại lệ khi dữ liệu lịch hẹn không hợp lệ."""
    pass
