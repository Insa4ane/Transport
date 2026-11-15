from Database.exceptions import BookingNotFound, RideAlreadyDeparted
from Database.models import Booking, User
from Database.repositories.booking_repository import BookingRepository

from ..errors import BadRequest, NotFound
from ..timeutils import now_utc, to_utc_iso


class BookingService:
    def __init__(self, bookings: BookingRepository):
        self._bookings = bookings

    def list_for_user(self, user: User) -> list[Booking]:
        return self._bookings.get_for_user(user.id)

    def cancel(self, booking_id: int, user: User) -> None:
        try:
            self._bookings.cancel(booking_id, user.id, to_utc_iso(now_utc()))
        except BookingNotFound:
            raise NotFound("Nie znaleziono rezerwacji") from None
        except RideAlreadyDeparted:
            raise BadRequest("Nie można odwołać rezerwacji po odjeździe") from None
