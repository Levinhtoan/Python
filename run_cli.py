"""Script tiện lợi để chạy ứng dụng CLI trực tiếp từ thư mục gốc."""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from booking_app.cli import main

if __name__ == "__main__":
    main()
