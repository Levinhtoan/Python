from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from booking_app.api.deps import get_booking_service
from booking_app.core.exceptions import (
    BookingNotFoundException,
    BookingValidationException,
)
from booking_app.schemas.booking import (
    BookingCreate,
    BookingResponse,
)
from booking_app.services.booking_service import BookingService

router = APIRouter()

@router.get("", response_model=List[BookingResponse], summary="Lấy danh sách tất cả lịch hẹn")
def read_bookings(service: BookingService = Depends(get_booking_service)):
    """Lấy danh sách toàn bộ các lịch hẹn đã lưu trong hệ thống."""
    return service.list_all_bookings()

@router.get("/{booking_id}", response_model=BookingResponse, summary="Chi tiết một lịch hẹn")
def read_booking(booking_id: int, service: BookingService = Depends(get_booking_service)):
    """Tìm thông tin lịch hẹn theo mã định danh (ID)."""
    try:
        return service.get_booking(booking_id)
    except BookingNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo mới một lịch hẹn",
)
def create_booking(
    booking_in: BookingCreate,
    service: BookingService = Depends(get_booking_service),
):
    """Tạo mới một lịch hẹn cho khách hàng."""
    try:
        return service.create_booking(booking_in)
    except BookingValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{booking_id}/cancel", response_model=BookingResponse, summary="Hủy lịch hẹn")
def cancel_booking(booking_id: int, service: BookingService = Depends(get_booking_service)):
    """Chuyển trạng thái lịch hẹn sang CANCELLED."""
    try:
        return service.cancel_booking(booking_id)
    except BookingNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{booking_id}", status_code=status.HTTP_200_OK, summary="Xóa vĩnh viễn lịch hẹn")
def delete_booking(booking_id: int, service: BookingService = Depends(get_booking_service)):
    """Xóa bỏ lịch hẹn khỏi hệ thống."""
    try:
        service.delete_booking(booking_id)
        return {"message": f"Đã xóa thành công lịch hẹn ID: {booking_id}"}
    except BookingNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
