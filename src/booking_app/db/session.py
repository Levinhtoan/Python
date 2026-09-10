from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from booking_app.core.config import settings

# Base model cho Declarative ORM
Base = declarative_base()

# Cấu hình engine kết nối PostgreSQL hoặc bất kỳ SQL Database nào qua sync_database_url
engine_kwargs = {"pool_pre_ping": True}
if settings.sync_database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update({
        "pool_size": 10,
        "max_overflow": 20,
    })

engine = create_engine(settings.sync_database_url, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager an toàn để cấp phát và đóng SQLAlchemy Session."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db(target_engine=None):
    """Khởi tạo toàn bộ các bảng trong cơ sở dữ liệu nếu chưa tồn tại."""
    # Import tất cả models trước khi create_all để metadata được đăng ký
    import booking_app.models.booking  # noqa: F401
    
    eng = target_engine or engine
    Base.metadata.create_all(bind=eng)
