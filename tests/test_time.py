from datetime import datetime

from safe_bit.constants import KEY_VALIDITY
from safe_bit.key import key
from safe_bit.time import get_date_from_time, get_time


def test_get_time_at_origin(t0_datetime: datetime):
    assert get_time(t0_datetime) == 0

def test_get_date_from_time(t0_datetime: datetime):
    assert get_date_from_time(0) == t0_datetime

def test_key_validity():
    k = key(1)
    assert k.valid_until - k.valid_from == KEY_VALIDITY
