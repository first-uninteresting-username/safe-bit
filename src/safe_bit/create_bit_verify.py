from base64 import b64decode, b64encode
from hashlib import sha512

from .key import Key
from .random_generation import (
    generate_random_byte_sequence_from_secret,
    hash_secret_minute,
)


def _compute_commitment_and_bit(
    secret: str, timestamp: int, key: Key
) -> tuple[str, int]:
    s = b64decode(secret)
    e = key.encrypt_minute(timestamp)
    h1 = hash_secret_minute(s, e)
    byte = generate_random_byte_sequence_from_secret(s, key, timestamp, 1)
    bit = byte[0] & 1
    h2 = sha512(h1 + bytes([bit])).digest()
    commitment = b64encode(h2).decode("ascii")

    return commitment, bit


def create_commited_bit(
    secret: str, timestamp: int, key: Key
) -> tuple[str, int, int]:
    # Use the stored key for this timestamp again when verifying the commitment.
    commitment, bit = _compute_commitment_and_bit(secret, timestamp, key)
    return commitment, bit, timestamp


def verify_bit(
    commitment: str, bit: int, timestamp: int, secret: str, key: Key
) -> bool:
    computed_commitment, computed_bit = _compute_commitment_and_bit(
        secret, timestamp, key
    )

    if bit != computed_bit:
        return False
    return commitment == computed_commitment
