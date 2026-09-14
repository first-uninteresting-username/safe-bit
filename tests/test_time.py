from datetime import datetime

from safe_bit.time import get_date_from_time, get_key_valid_until, get_time


def test_get_time_at_origin(t0_datetime: datetime):
    assert get_time(t0_datetime) == 0


def test_get_key_valid_until(t0_datetime: datetime):
    assert get_key_valid_until(t0_datetime) == 10080

def test_get_date_from_time(t0_datetime: datetime):
    assert get_date_from_time(0) == t0_datetime
