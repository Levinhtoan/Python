from abc import ABC, abstractmethod
from typing import List, Optional
from booking_app.schemas.booking import BookingResponse, BookingCreate, BookingUpdate

class BaseBookingRepository(ABC):
    """Giao diện trừu tượng cho kho lưu trữ dữ liệu (Repository Pattern)."""

    @abstractmethod
    def get_all(self) -> List[BookingResponse]:
        pass

    @abstractmethod
    def get_by_id(self, booking_id: int) -> Optional[BookingResponse]:
        pass

    @abstractmethod
    def create(self, booking: BookingCreate) -> BookingResponse:
        pass

    @abstractmethod
    def update(self, booking_id: int, booking_update: BookingUpdate) -> Optional[BookingResponse]:
        pass

    @abstractmethod
    def delete(self, booking_id: int) -> bool:
        pass
