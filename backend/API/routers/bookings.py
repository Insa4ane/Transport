from fastapi import APIRouter, Depends, Response

from Database.models import User

from ..dependencies import get_booking_service, require_passenger
from ..schemas.bookings import BookingOut
from ..services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", response_model=list[BookingOut])
def my_bookings(
    passenger: User = Depends(require_passenger),
    bookings: BookingService = Depends(get_booking_service),
):
    return bookings.list_for_user(passenger)


@router.delete("/{booking_id}", status_code=204)
def cancel_booking(
    booking_id: int,
    passenger: User = Depends(require_passenger),
    bookings: BookingService = Depends(get_booking_service),
):
    bookings.cancel(booking_id, passenger)
    return Response(status_code=204)
