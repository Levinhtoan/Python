from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from booking_app.core.config import settings
from booking_app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Quản lý vòng đời khởi động và kết thúc của ứng dụng."""
    if settings.DB_TYPE == "postgres":
        try:
            from booking_app.db.session import init_db
            init_db()
        except Exception as e:
            print(f"⚠️ Không thể tự động khởi tạo bảng DB (vui lòng kiểm tra kết nối PostgreSQL): {e}")
    yield

def create_app() -> FastAPI:
    """Application Factory khởi tạo ứng dụng FastAPI."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Hệ thống quản lý đặt lịch chuẩn Clean Architecture theo tài liệu PYTHON_PROJECT_STRUCTURE.md",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )


    # Cấu hình CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Đăng ký Router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    @application.get("/", tags=["Hệ thống"])
    def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "docs": "/docs",
            "status": "running"
        }

    return application

app = create_app()

if __name__ == "__main__":
    uvicorn.run("booking_app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
