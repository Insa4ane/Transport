from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from Database.models import User

from .container import container
from .errors import Forbidden, Unauthorized
from .services.auth_service import AuthService
from .services.booking_service import BookingService
from .services.ride_service import RideService

bearer = HTTPBearer(auto_error=False)


def get_auth_service() -> AuthService:
    return container.auth_service


def get_ride_service() -> RideService:
    return container.ride_service


def get_booking_service() -> BookingService:
    return container.booking_service


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    auth: AuthService = Depends(get_auth_service),
) -> User:
    if credentials is None:
        raise Unauthorized()
    return auth.user_from_token(credentials.credentials)


def require_driver(user: User = Depends(get_current_user)) -> User:
    if not user.is_driver:
        raise Forbidden("Tylko kierowcy mogą dodawać przejazdy")
    return user


def require_passenger(user: User = Depends(get_current_user)) -> User:
    if user.is_driver:
        raise Forbidden("Kierowcy nie mogą rezerwować przejazdów")
    return user
