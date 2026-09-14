from datetime import datetime

from safe_bit.time import get_time


def test_get_time_at_origin(t0_datetime: datetime):
    assert get_time(t0_datetime) == 0
