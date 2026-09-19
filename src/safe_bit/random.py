from hashlib import sha512
from random import Random

from .key import key


def hash_two_strings(s1: str, s2: str) -> str:
    string = s1 + s2
    b = string.encode("utf-8")
    digest = sha512(b).hexdigest()
    return digest

def generate_random_bit_sequence(secret: str, key: key, len: int) -> bytes:
    current = key.current
    hash = hash_two_strings(secret, current)
    rng = Random(hash)
    sequence = rng.randbytes(len)
    return sequence
