from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    username: str
    password_hash: str
    is_driver: bool


@dataclass(frozen=True)
class Ride:
    id: int
    origin: str
    destination: str
    departure: str  
    seats_left: int
    price: float
    driver_name: str


@dataclass(frozen=True)
class Booking:
    id: int
    seats: int
    ride_id: int
    origin: str
    destination: str
    departure: str
    price: float
    driver_name: str
