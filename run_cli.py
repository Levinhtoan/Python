import os
import sys

# Thêm src vào sys.path để import booking_app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from booking_app.cli import main


if __name__ == "__main__":
    main()
