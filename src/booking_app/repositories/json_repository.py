import json
import os
from datetime import datetime
from typing import List, Optional
from booking_app.repositories.base import BaseBookingRepository
from booking_app.schemas.booking import (
    BookingResponse,
    BookingCreate,
    BookingUpdate,
    BookingStatus,
)

class JSONBookingRepository(BaseBookingRepository):
    """Triển khai lưu trữ lịch hẹn bằng file JSON bền vững (Persistent Storage)."""

    def __init__(self, file_path: str = "data/bookings.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        dir_name = os.path.dirname(self.file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_data(self) -> List[dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_all(self) -> List[BookingResponse]:
        raw_list = self._read_data()
        return [BookingResponse(**item) for item in raw_list]

    def get_by_id(self, booking_id: int) -> Optional[BookingResponse]:
        raw_list = self._read_data()
        for item in raw_list:
            if item["id"] == booking_id:
                return BookingResponse(**item)
        return None

    def create(self, booking_in: BookingCreate) -> BookingResponse:
        raw_list = self._read_data()
        new_id = (raw_list[-1]["id"] + 1) if raw_list else 1
        new_item = {
            "id": new_id,
            "customer": booking_in.customer,
            "service": booking_in.service,
            "time": booking_in.time,
            "notes": booking_in.notes,
            "status": BookingStatus.CONFIRMED.value,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        raw_list.append(new_item)
        self._write_data(raw_list)
        return BookingResponse(**new_item)

    def update(self, booking_id: int, booking_update: BookingUpdate) -> Optional[BookingResponse]:
        raw_list = self._read_data()
        for index, item in enumerate(raw_list):
            if item["id"] == booking_id:
                update_data = booking_update.model_dump(exclude_unset=True)
                for key, val in update_data.items():
                    if val is not None:
                        item[key] = val.value if hasattr(val, "value") else val
                raw_list[index] = item
                self._write_data(raw_list)
                return BookingResponse(**item)
        return None

    def delete(self, booking_id: int) -> bool:
        raw_list = self._read_data()
        for index, item in enumerate(raw_list):
            if item["id"] == booking_id:
                raw_list.pop(index)
                self._write_data(raw_list)
                return True
        return False
