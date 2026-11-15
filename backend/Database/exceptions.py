class UserAlreadyExists(Exception):
    """Login jest już zajęty."""


class RideNotFound(Exception):
    """Przejazd o podanym id nie istnieje."""


class NotEnoughSeats(Exception):
    """Brak wystarczającej liczby wolnych miejsc."""

    def __init__(self, seats_left: int):
        super().__init__(f"Dostępnych miejsc: {seats_left}")
        self.seats_left = seats_left


class BookingNotFound(Exception):
    """Rezerwacja nie istnieje albo należy do kogoś innego."""


class RideAlreadyDeparted(Exception):
    """Przejazd już się odbył, więc rezerwacji nie można odwołać."""
