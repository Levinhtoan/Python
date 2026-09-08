from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class BookingStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class BookingBase(BaseModel):
    customer: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Tên khách hàng",
        json_schema_extra={"example": "Nguyễn Văn A"}
    )
    service: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Tên dịch vụ",
        json_schema_extra={"example": "Cắt tóc tạo kiểu"}
    )
    time: str = Field(
        ...,
        description="Thời gian hẹn (VD: 2026-09-10 14:30)",
        json_schema_extra={"example": "2026-09-10 14:30"}
    )
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Ghi chú thêm",
        json_schema_extra={"example": "Khách thích gội đầu thảo dược"}
    )

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    customer: Optional[str] = None
    service: Optional[str] = None
    time: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[BookingStatus] = None

class BookingResponse(BookingBase):
    id: int
    status: BookingStatus = BookingStatus.CONFIRMED
    created_at: str

    model_config = ConfigDict(from_attributes=True)

