from datetime import UTC, datetime, timedelta
from math import floor

from .constants import T0


def get_time(dt: datetime) -> int:
    diff = dt - T0
    total_minutes = floor(diff.total_seconds() / 60)
    return int(total_minutes)

def get_date_from_time(t: int) -> datetime:
    return T0 + timedelta(minutes=t)

def get_current_time() -> int:
    now = datetime.now(UTC)
    now_int = get_time(now)
    return now_int
