from datetime import datetime, timezone


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def as_utc(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def to_utc_iso(dt: datetime) -> str:
    return as_utc(dt).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
