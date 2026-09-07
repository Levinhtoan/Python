from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uvicorn

# 1. Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Booking & Scheduling API",
    description="API đơn giản quản lý đặt lịch hẹn sử dụng FastAPI",
    version="1.0.0"
)

# 2. Định nghĩa Schema (Khuôn mẫu dữ liệu) với Pydantic
class BookingCreate(BaseModel):
    customer: str = Field(..., example="Nguyễn Văn A", description="Tên khách hàng")
    service: str = Field(..., example="Cắt tóc tạo kiểu", description="Tên dịch vụ")
    time: str = Field(..., example="2026-09-10 14:30", description="Thời gian hẹn")
    notes: Optional[str] = Field(None, example="Gội đầu thảo dược", description="Ghi chú thêm")

class Booking(BaseModel):
    id: int
    customer: str
    service: str
    time: str
    notes: Optional[str] = None
    status: str = "CONFIRMED"
    created_at: str

# 3. Dữ liệu mẫu (Database tạm thời trong bộ nhớ)
db_bookings: List[Booking] = [
    Booking(
        id=1,
        customer="Trần Thị Mai",
        service="Chăm sóc da mặt",
        time="2026-09-10 09:00",
        notes="Da nhạy cảm",
        status="CONFIRMED",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ),
    Booking(
        id=2,
        customer="Lê Văn B",
        service="Cắt tóc",
        time="2026-09-10 15:00",
        notes=None,
        status="CONFIRMED",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
]

# ==========================================
# 4. CÁC API ENDPOINTS (ROUTES)
# ==========================================

@app.get("/", tags=["Trang chủ"])
def read_root():
    """Trang chủ kiểm tra trạng thái API."""
    return {
        "message": "Chào mừng bạn đến với Booking API!",
        "docs_url": "http://127.0.0.1:8000/docs",
        "status": "online"
    }

@app.get("/bookings", response_model=List[Booking], tags=["Đặt lịch"])
def get_all_bookings():
    """Lấy toàn bộ danh sách lịch hẹn."""
    return db_bookings

@app.get("/bookings/{booking_id}", response_model=Booking, tags=["Đặt lịch"])
def get_booking_by_id(booking_id: int):
    """Tìm lịch hẹn theo mã ID."""
    for booking in db_bookings:
        if booking.id == booking_id:
            return booking
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy lịch hẹn với ID: {booking_id}"
    )

@app.post("/bookings", response_model=Booking, status_code=status.HTTP_201_CREATED, tags=["Đặt lịch"])
def create_booking(payload: BookingCreate):
    """Tạo mới một lịch hẹn."""
    new_id = (db_bookings[-1].id + 1) if db_bookings else 1
    new_booking = Booking(
        id=new_id,
        customer=payload.customer,
        service=payload.service,
        time=payload.time,
        notes=payload.notes,
        status="CONFIRMED",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db_bookings.append(new_booking)
    return new_booking

@app.put("/bookings/{booking_id}/cancel", response_model=Booking, tags=["Đặt lịch"])
def cancel_booking(booking_id: int):
    """Hủy một lịch hẹn."""
    for booking in db_bookings:
        if booking.id == booking_id:
            booking.status = "CANCELLED"
            return booking
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy lịch hẹn với ID: {booking_id}"
    )

@app.delete("/bookings/{booking_id}", tags=["Đặt lịch"])
def delete_booking(booking_id: int):
    """Xóa hoàn toàn lịch hẹn khỏi hệ thống."""
    for index, booking in enumerate(db_bookings):
        if booking.id == booking_id:
            db_bookings.pop(index)
            return {"message": f"Đã xóa thành công lịch hẹn ID: {booking_id}"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy lịch hẹn với ID: {booking_id}"
    )

# 5. Chạy ứng dụng trực tiếp bằng lệnh: python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
