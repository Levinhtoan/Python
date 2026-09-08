from fastapi import APIRouter
from booking_app.api.v1.endpoints import bookings

api_router = APIRouter()
api_router.include_router(bookings.router, prefix="/bookings", tags=["Đặt lịch (Bookings)"])
