from ..connection import Database
from ..exceptions import NotEnoughSeats, RideNotFound
from ..models import Ride


class RideRepository:

    _SELECT = """
    SELECT r.id, r.origin, r.destination, r.departure, r.seats_left, r.price,
           u.username AS driver_name
    FROM rides r
    JOIN users u ON u.id = r.driver_id
    """

    @staticmethod
    def _to_ride(row) -> Ride | None:
        if row is None:
            return None
        return Ride(
            id=row["id"],
            origin=row["origin"],
            destination=row["destination"],
            departure=row["departure"],
            seats_left=row["seats_left"],
            price=row["price"],
            driver_name=row["driver_name"],
        )

    def __init__(self, db: Database):
        self._db = db

    def create(
        self, driver_id: int, origin: str, destination: str, departure: str, seats: int, price: float
    ) -> Ride:
        query = """
        INSERT INTO rides (driver_id, origin, destination, departure, seats_left, price)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        with self._db.transaction() as conn:
            ride_id = conn.execute(
                query, (driver_id, origin, destination, departure, seats, price)
            ).lastrowid
        return self.get(ride_id)

    def get(self, ride_id: int) -> Ride | None:
        row = self._db.fetch_one(self._SELECT + " WHERE r.id = ?", (ride_id,))
        return self._to_ride(row)

    def get_all(self, origin: str = "", destination: str = "") -> list[Ride]:
        query = self._SELECT + """
        WHERE instr(fold(r.origin), ?) > 0
          AND instr(fold(r.destination), ?) > 0
        ORDER BY r.departure
        """
        params = (origin.strip().casefold(), destination.strip().casefold())
        return [self._to_ride(row) for row in self._db.fetch_all(query, params)]

    def book(self, ride_id: int, user_id: int, seats: int) -> Ride:
        if seats < 1:
            raise ValueError("Liczba miejsc musi być dodatnia")

        with self._db.transaction() as conn:
            updated = conn.execute(
                "UPDATE rides SET seats_left = seats_left - ? WHERE id = ? AND seats_left >= ?",
                (seats, ride_id, seats),
            ).rowcount
            if updated == 0:
                # Nic nie zmieniono: albo nie ma takiego przejazdu, albo brak miejsc.
                row = conn.execute(
                    "SELECT seats_left FROM rides WHERE id = ?", (ride_id,)
                ).fetchone()
                if row is None:
                    raise RideNotFound(ride_id)
                raise NotEnoughSeats(row["seats_left"])

            conn.execute(
                "INSERT INTO bookings (ride_id, user_id, seats) VALUES (?, ?, ?)",
                (ride_id, user_id, seats),
            )
        return self.get(ride_id)
