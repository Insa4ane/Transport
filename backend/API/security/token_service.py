from datetime import timedelta
import jwt
from ..timeutils import now_utc
from .exceptions import InvalidToken


class TokenService:
    def __init__(self, secret_key: str, algorithm: str = "HS256", ttl_hours: int = 12):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._ttl = timedelta(hours=ttl_hours)

    def create(self, user_id: int) -> str:
        payload = {"sub": str(user_id), "exp": now_utc() + self._ttl}
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def read_user_id(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return int(payload["sub"])
        except (jwt.PyJWTError, KeyError, ValueError):
            raise InvalidToken from None
