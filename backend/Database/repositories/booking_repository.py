from ..connection import Database
from ..exceptions import BookingNotFound, RideAlreadyDeparted
from ..models import Booking


class BookingRepository:
    def __init__(self, db: Database):
        self._db = db

    def get_for_user(self, user_id: int) -> list[Booking]:
        query = """
        SELECT b.id, b.seats, b.ride_id, r.origin, r.destination, r.departure, r.price,
               u.username AS driver_name
        FROM bookings b
        JOIN rides r ON r.id = b.ride_id
        JOIN users u ON u.id = r.driver_id
        WHERE b.user_id = ?
        ORDER BY r.departure
        """
        return [
            Booking(
                id=row["id"],
                seats=row["seats"],
                ride_id=row["ride_id"],
                origin=row["origin"],
                destination=row["destination"],
                departure=row["departure"],
                price=row["price"],
                driver_name=row["driver_name"],
            )
            for row in self._db.fetch_all(query, (user_id,))
        ]

    def cancel(self, booking_id: int, user_id: int, now: str) -> None:
        """Usuwa rezerwację i oddaje miejsca przejazdowi (w jednej transakcji).

        Rzuca BookingNotFound (też gdy rezerwacja jest cudza, żeby nie zdradzać cudzych id)
        albo RideAlreadyDeparted. `now` w tym samym formacie co kolumna departure.
        """
        with self._db.transaction() as conn:
            row = conn.execute(
                """
                SELECT b.ride_id, b.seats, r.departure
                FROM bookings b JOIN rides r ON r.id = b.ride_id
                WHERE b.id = ? AND b.user_id = ?
                """,
                (booking_id, user_id),
            ).fetchone()
            if row is None:
                raise BookingNotFound(booking_id)
            if row["departure"] <= now:
                raise RideAlreadyDeparted(booking_id)

            conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
            conn.execute(
                "UPDATE rides SET seats_left = seats_left + ? WHERE id = ?",
                (row["seats"], row["ride_id"]),
            )
