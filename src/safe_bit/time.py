from datetime import UTC, datetime, timedelta

from .variables import T0


def get_time(dt: datetime) -> int:
    return (dt - T0) // timedelta(minutes=1)


def get_date_from_time(t: int) -> datetime:
    return T0 + timedelta(minutes=t)


def get_current_time() -> int:
    now = datetime.now(UTC)
    now_int = get_time(now)
    return now_int
