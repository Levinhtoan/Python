from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from booking_app.db.session import Base
from booking_app.schemas.booking import BookingStatus, BookingResponse

class BookingModel(Base):
    """Bảng lưu trữ thông tin đặt lịch hẹn trong cơ sở dữ liệu PostgreSQL/SQL."""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer = Column(String(100), nullable=False, index=True)
    service = Column(String(100), nullable=False)
    time = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default=BookingStatus.CONFIRMED.value, nullable=False)
    created_at = Column(String(50), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nullable=False)

    def to_schema(self) -> BookingResponse:
        """Chuyển đổi từ ORM Model sang Pydantic Response Schema."""
        return BookingResponse(
            id=self.id,
            customer=self.customer,
            service=self.service,
            time=self.time,
            notes=self.notes,
            status=BookingStatus(self.status) if isinstance(self.status, str) else self.status,
            created_at=str(self.created_at),
        )
