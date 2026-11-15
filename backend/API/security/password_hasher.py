import bcrypt

class PasswordHasher:
    def __init__(self, max_bytes: int = 72):
        self._max_bytes = max_bytes
        self.dummy_hash = self.hash("dummy-password")

    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify(self, password: str, password_hash: str) -> bool:
        raw = password.encode("utf-8")
        if len(raw) > self._max_bytes:  
            return False
        return bcrypt.checkpw(raw, password_hash.encode("utf-8"))
