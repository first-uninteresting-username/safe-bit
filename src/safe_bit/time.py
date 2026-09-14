from datetime import UTC, datetime, timedelta
from math import floor

# Sep 14 2026 00:00:00 UTC
# 1789344000
t0 = datetime(2026, 9, 14, 0, 0, 0, tzinfo=UTC)


def get_time(date_time: datetime) -> int:
    diff = date_time - t0
    total_minutes = floor(diff.total_seconds() / 60)
    return int(total_minutes)

def get_key_expiration_date(date_time: datetime) -> int:
    diff = date_time - t0
    total_minutes = floor(diff.total_seconds() / 60)
    return int(total_minutes) + 10080  # 7 days

def get_date_from_time(time: int) -> datetime:
    return t0 + timedelta(minutes=time)
