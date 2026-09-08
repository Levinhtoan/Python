"""Script tiện lợi để khởi chạy FastAPI Server từ thư mục gốc."""
import sys

# Đảm bảo in UTF-8 không lỗi font/emoji trên Windows Console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import uvicorn
from booking_app.core.config import settings

if __name__ == "__main__":
    print(f"🚀 Khởi động {settings.PROJECT_NAME} trên http://{settings.HOST}:{settings.PORT}")
    print(f"📖 Swagger Docs: http://{settings.HOST}:{settings.PORT}/docs")
    uvicorn.run("booking_app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
