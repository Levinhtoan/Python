import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from booking_app.repositories.json_repository import JSONBookingRepository
from booking_app.services.booking_service import BookingService
from booking_app.main import create_app
from booking_app.api.deps import get_booking_service

@pytest.fixture
def temp_json_file():
    """Tạo một file json tạm thời cho mỗi test case để tránh làm bẩn dữ liệu thật."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def test_repo(temp_json_file):
    """Fixture cung cấp JSONBookingRepository độc lập."""
    return JSONBookingRepository(file_path=temp_json_file)

@pytest.fixture
def test_service(test_repo):
    """Fixture cung cấp BookingService độc lập."""
    return BookingService(repository=test_repo)

@pytest.fixture
def client(test_service):
    """TestClient cho FastAPI với mocked service."""
    app = create_app()
    app.dependency_overrides[get_booking_service] = lambda: test_service
    with TestClient(app) as test_client:
        yield test_client
