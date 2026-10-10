from collections.abc import Iterator
from hashlib import sha512

from .key import key


class SeedTooBigError(ValueError):
    pass

# The implementation might be changed, but the algorithm must stay the same
def _generate_byte_sequence(seed: int, count: int) -> Iterator[int]:
    if not 0 <= seed < 4294967296:
        raise SeedTooBigError("Seed must be between 0 and 4294967295")

    s = seed
    for _ in range(count):
            s = (1664525 * s + 1013904223) % 4294967296
            yield s // 16777216

def hash_secret_minute(secret: bytes, minute: bytes) -> bytes:
    length_prefix = len(secret).to_bytes(4, "big")
    b = length_prefix + secret + minute
    digest = sha512(b).digest()
    return digest

def generate_random_byte_sequence_from_secret(secret: bytes, key: key, timestamp: int, length: int = 1) -> bytes:
    minute = key.encrypt_minute(timestamp)
    hash = hash_secret_minute(secret, minute)
    sequence = bytes(_generate_byte_sequence(int.from_bytes(hash, "big") % 4294967296, length))
    return sequence
