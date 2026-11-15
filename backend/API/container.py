from Database.connection import Database
from Database.repositories.booking_repository import BookingRepository
from Database.repositories.ride_repository import RideRepository
from Database.repositories.user_repository import UserRepository

from . import config
from .security.password_hasher import PasswordHasher
from .security.token_service import TokenService
from .services.auth_service import AuthService
from .services.booking_service import BookingService
from .services.ride_service import RideService


class Container:
    def __init__(self):
        self.db = Database(config.DB_PATH)
        self.users = UserRepository(self.db)
        self.rides = RideRepository(self.db)
        self.bookings = BookingRepository(self.db)
        self.hasher = PasswordHasher(config.MAX_PASSWORD_BYTES)
        self.tokens = TokenService(config.SECRET_KEY, config.JWT_ALGORITHM, config.TOKEN_HOURS)
        self.auth_service = AuthService(self.users, self.hasher, self.tokens)
        self.ride_service = RideService(self.rides)
        self.booking_service = BookingService(self.bookings)


container = Container()
