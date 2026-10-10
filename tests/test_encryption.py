from random import randint

from safe_bit.constants import KEY_VALIDITY
from safe_bit.key import key


def test_encryption_for_all():
    n = randint(1, KEY_VALIDITY)
    k = key(n)
    numbers = range(k.valid_from, k.valid_until + 1)
    for i in numbers:
        assert k.encrypt_minute(i) == k.encrypt_minute(i) == k.encrypt_minute(i)

def test_two_minutes_dif_results():
    n = randint(1, KEY_VALIDITY)
    k = key(n)
    n1 = randint(k.valid_from, k.valid_until)
    n2 = randint(k.valid_from, k.valid_until)
    while n1 == n2:
        n2 = randint(k.valid_from, k.valid_until)
    assert k.encrypt_minute(n1) != k.encrypt_minute(n2)
    assert k.encrypt_minute(n1 + 1) != k.encrypt_minute(n2 + 1)
