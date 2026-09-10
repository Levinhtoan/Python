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
def test_postgres_repo():
    """Fixture cung cấp PostgresBookingRepository sử dụng SQLite in-memory database để test."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from booking_app.db.session import Base
    from booking_app.repositories.postgres_repository import PostgresBookingRepository
    import booking_app.models.booking  # noqa: F401

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    repo = PostgresBookingRepository(session_factory=testing_session_local)
    yield repo
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_service):
    """TestClient cho FastAPI với mocked service."""
    app = create_app()
    app.dependency_overrides[get_booking_service] = lambda: test_service
    with TestClient(app) as test_client:
        yield test_client

