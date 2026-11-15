import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent

APP_TITLE = "Wspólne przejazdy API"
API_PREFIX = "/api"

DB_PATH = os.environ.get("DB_PATH", str(BACKEND_DIR / "Database" / "app.db"))

DEV_SECRET_KEY = "dev-only-secret-change-me-0123456789abcdef"
SECRET_KEY = os.environ.get("SECRET_KEY", DEV_SECRET_KEY)
if SECRET_KEY == DEV_SECRET_KEY:
    print("UWAGA: brak zmiennej SECRET_KEY, używam klucza deweloperskiego.")

JWT_ALGORITHM = "HS256"
TOKEN_HOURS = 12             
MAX_PASSWORD_BYTES = 72     

_DEFAULT_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173" 
CORS_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CORS_ORIGINS", _DEFAULT_ORIGINS).split(",")
    if origin.strip()
]

USERNAME_MIN = 3
USERNAME_MAX = 30
PASSWORD_MIN = 8
PASSWORD_MAX = 128
CITY_MIN = 2
CITY_MAX = 60
MAX_SEATS = 8
MAX_PRICE = 100_000
