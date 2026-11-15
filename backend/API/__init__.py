"""Pakiet API. Dodaje katalog backend/ do ścieżki importów,
dzięki czemu działa `from Database... import ...` niezależnie od miejsca uruchomienia."""
import sys
from pathlib import Path

_BACKEND_DIR = str(Path(__file__).resolve().parent.parent)
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)
