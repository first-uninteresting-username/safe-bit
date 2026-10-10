from hashlib import sha512

from .key import key
from .random_generation import (
    generate_random_byte_sequence_from_secret,
    hash_secret_minute,
)


def create_commited_bit(secret: bytes, key: key, timestamp: int) -> tuple[bytes, int, int] | None:
    e = key.encrypt_minute(timestamp)
    h1 = hash_secret_minute(secret, e)
    byte = generate_random_byte_sequence_from_secret(secret, key, timestamp, 1)
    bit = byte[0] & 1
    h2 = sha512(h1 + bytes(bit)).digest()
    return h2, bit, timestamp
