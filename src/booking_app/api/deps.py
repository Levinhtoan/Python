from functools import lru_cache
from booking_app.core.config import settings
from booking_app.repositories.json_repository import JSONBookingRepository
from booking_app.services.booking_service import BookingService

@lru_cache()
def get_repository() -> JSONBookingRepository:
    """Tạo Singleton Repository lưu trữ."""
    return JSONBookingRepository(file_path=settings.DATA_FILE_PATH)

def get_booking_service() -> BookingService:
    """Dependency Injection cung cấp instance của BookingService."""
    repo = get_repository()
    return BookingService(repository=repo)
