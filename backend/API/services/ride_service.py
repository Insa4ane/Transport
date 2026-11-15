from datetime import datetime

from Database.exceptions import NotEnoughSeats, RideNotFound
from Database.models import Ride, User
from Database.repositories.ride_repository import RideRepository

from ..errors import BadRequest, NotFound
from ..timeutils import to_utc_iso


class RideService:
    """Przejazdy i rezerwacje."""

    def __init__(self, rides: RideRepository):
        self._rides = rides

    def list_rides(self, origin: str = "", destination: str = "") -> list[Ride]:
        return self._rides.get_all(origin, destination)

    def get_ride(self, ride_id: int) -> Ride:
        ride = self._rides.get(ride_id)
        if ride is None:
            raise NotFound("Nie znaleziono przejazdu")
        return ride

    def create_ride(
        self,
        driver: User,
        origin: str,
        destination: str,
        departure: datetime,
        seats: int,
        price: float,
    ) -> Ride:
        return self._rides.create(
            driver_id=driver.id, 
            origin=origin,
            destination=destination,
            departure=to_utc_iso(departure),
            seats=seats,
            price=price,
        )

    def book_ride(self, ride_id: int, passenger: User, seats: int) -> Ride:
        try:
            return self._rides.book(ride_id, passenger.id, seats)
        except RideNotFound:
            raise NotFound("Nie znaleziono przejazdu") from None
        except NotEnoughSeats as error:
            raise BadRequest(f"Dostępnych miejsc: {error.seats_left}") from None
