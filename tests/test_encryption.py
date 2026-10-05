from safe_bit.constants import KEY_VALIDITY
from safe_bit.key import key


def test_encryption():
    k = key(KEY_VALIDITY)
    numbers = range(k.valid_until, k.valid_from + 1)
    for i in numbers:
        assert k.encrypt_minute(i) == k.encrypt_minute(i) == k.encrypt_minute(i)
