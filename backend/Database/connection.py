import sqlite3
import threading
from contextlib import contextmanager

from .schema import SCHEMA


class Database:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.create_function(
            "fold", 1, lambda s: s.casefold() if s else s, deterministic=True
        )
        self._lock = threading.RLock()
        self._create_schema()

    def _create_schema(self) -> None:
        with self.transaction() as conn:
            for statement in SCHEMA:
                conn.execute(statement)

    @contextmanager
    def transaction(self):
        with self._lock:
            try:
                yield self.conn
                self.conn.commit()
            except Exception:
                self.conn.rollback()
                raise

    def fetch_one(self, sql: str, params: tuple = ()):
        with self._lock:
            return self.conn.execute(sql, params).fetchone()

    def fetch_all(self, sql: str, params: tuple = ()):
        with self._lock:
            return self.conn.execute(sql, params).fetchall()

    def close(self) -> None:
        with self._lock:
            self.conn.close()
