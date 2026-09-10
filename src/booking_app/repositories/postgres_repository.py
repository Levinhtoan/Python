from contextlib import contextmanager
from typing import List, Optional, Callable, Generator
from sqlalchemy.orm import Session, sessionmaker
from booking_app.repositories.base import BaseBookingRepository
from booking_app.schemas.booking import (
    BookingResponse,
    BookingCreate,
    BookingUpdate,
    BookingStatus,
)
from booking_app.models.booking import BookingModel
from booking_app.db.session import SessionLocal

class PostgresBookingRepository(BaseBookingRepository):
    """Triển khai lưu trữ lịch hẹn bằng cơ sở dữ liệu quan hệ PostgreSQL (SQLAlchemy ORM)."""

    def __init__(self, session_factory: Optional[Callable[[], Session]] = None):
        self.session_factory = session_factory or SessionLocal

    @contextmanager
    def _get_session(self) -> Generator[Session, None, None]:
        """Cung cấp session an toàn với tự động commit/rollback."""
        session: Session = self.session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_all(self) -> List[BookingResponse]:
        with self._get_session() as session:
            records = session.query(BookingModel).order_by(BookingModel.id.asc()).all()
            return [rec.to_schema() for rec in records]

    def get_by_id(self, booking_id: int) -> Optional[BookingResponse]:
        with self._get_session() as session:
            record = session.query(BookingModel).filter(BookingModel.id == booking_id).first()
            if record:
                return record.to_schema()
            return None

    def create(self, booking: BookingCreate) -> BookingResponse:
        with self._get_session() as session:
            db_booking = BookingModel(
                customer=booking.customer,
                service=booking.service,
                time=booking.time,
                notes=booking.notes,
                status=BookingStatus.CONFIRMED.value,
            )
            session.add(db_booking)
            session.commit()
            session.refresh(db_booking)
            return db_booking.to_schema()

    def update(self, booking_id: int, booking_update: BookingUpdate) -> Optional[BookingResponse]:
        with self._get_session() as session:
            record = session.query(BookingModel).filter(BookingModel.id == booking_id).first()
            if not record:
                return None
            
            update_data = booking_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if value is not None:
                    if hasattr(value, "value"):
                        value = value.value
                    setattr(record, field, value)
            
            session.commit()
            session.refresh(record)
            return record.to_schema()

    def delete(self, booking_id: int) -> bool:
        with self._get_session() as session:
            record = session.query(BookingModel).filter(BookingModel.id == booking_id).first()
            if not record:
                return False
            session.delete(record)
            session.commit()
            return True
