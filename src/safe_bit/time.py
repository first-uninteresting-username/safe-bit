from datetime import UTC, datetime, timedelta
from math import floor

# Sep 14 2026 00:00:00 UTC
# 1789344000
t0 = datetime(2026, 9, 14, 0, 0, 0, tzinfo=UTC)


def get_time(dt: datetime) -> int:
    diff = dt - t0
    total_minutes = floor(diff.total_seconds() / 60)
    return int(total_minutes)


def get_key_valid_until(dt: datetime) -> int:
    diff = dt - t0
    total_minutes = floor(diff.total_seconds() / 60)
    return int(total_minutes) + 10080  # 7 days


def get_date_from_time(t: int) -> datetime:
    return t0 + timedelta(minutes=t)
