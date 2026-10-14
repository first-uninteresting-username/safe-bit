from datetime import datetime
from pathlib import Path

from safe_bit.key_store import KeyStore
from safe_bit.time import get_date_from_time, get_time
from safe_bit.variables import KEY_VALIDITY


def test_get_time_at_origin(t0_datetime: datetime):
    assert get_time(t0_datetime) == 0


def test_get_date_from_time(t0_datetime: datetime):
    assert get_date_from_time(0) == t0_datetime


def test_key_validity(tmp_path: Path):
    k = KeyStore(tmp_path / "keys.db").generate_key_and_insert()
    assert k.valid_until - k.valid_from == KEY_VALIDITY
