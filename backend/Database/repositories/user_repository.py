import sqlite3

from ..connection import Database
from ..exceptions import UserAlreadyExists
from ..models import User


class UserRepository:
    def __init__(self, db: Database):
        self._db = db

    @staticmethod
    def _to_user(row) -> User | None:
        if row is None:
            return None
        return User(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            is_driver=bool(row["is_driver"]),
        )

    def create(self, username: str, password_hash: str, is_driver: bool = False) -> User:
        query = "INSERT INTO users (username, password_hash, is_driver) VALUES (?, ?, ?)"
        try:
            with self._db.transaction() as conn:
                user_id = conn.execute(query, (username, password_hash, int(is_driver))).lastrowid
        except sqlite3.IntegrityError:
            raise UserAlreadyExists(username) from None
        return self.get_by_id(user_id)

    def get_by_username(self, username: str) -> User | None:
        row = self._db.fetch_one(
            "SELECT id, username, password_hash, is_driver FROM users WHERE username = ?",
            (username,),
        )
        return self._to_user(row)

    def get_by_id(self, user_id: int) -> User | None:
        row = self._db.fetch_one(
            "SELECT id, username, password_hash, is_driver FROM users WHERE id = ?",
            (user_id,),
        )
        return self._to_user(row)
