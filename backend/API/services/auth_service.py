from Database.exceptions import UserAlreadyExists
from Database.models import User
from Database.repositories.user_repository import UserRepository

from ..errors import Conflict, Unauthorized
from ..security.exceptions import InvalidToken
from ..security.password_hasher import PasswordHasher
from ..security.token_service import TokenService


class AuthService:
    """Rejestracja, logowanie i rozpoznawanie użytkownika po tokenie."""

    def __init__(self, users: UserRepository, hasher: PasswordHasher, tokens: TokenService):
        self._users = users
        self._hasher = hasher
        self._tokens = tokens

    def register(self, username: str, password: str, is_driver: bool) -> User:
        try:
            return self._users.create(username, self._hasher.hash(password), is_driver)
        except UserAlreadyExists:
            raise Conflict("Ten login jest już zajęty") from None

    def login(self, username: str, password: str) -> tuple[str, User]:
        """Zwraca (token, użytkownik) albo rzuca Unauthorized."""
        user = self._users.get_by_username(username)
        stored_hash = user.password_hash if user else self._hasher.dummy_hash
        password_ok = self._hasher.verify(password, stored_hash)
        if user is None or not password_ok:
            raise Unauthorized("Nieprawidłowy login lub hasło")
        return self._tokens.create(user.id), user

    def user_from_token(self, token: str) -> User:
        try:
            user_id = self._tokens.read_user_id(token)
        except InvalidToken:
            raise Unauthorized() from None
        user = self._users.get_by_id(user_id)
        if user is None:
            raise Unauthorized()
        return user
