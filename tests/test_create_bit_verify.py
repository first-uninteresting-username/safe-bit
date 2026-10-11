from base64 import b64encode

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from safe_bit.create_bit_verify import create_commited_bit, verify_bit
from safe_bit.key import Key


def test_commitment_verifies_with_the_same_key():
    key = Key(ChaCha20Poly1305.generate_key(), 1, 1, 10)
    secret = b64encode(b"test secret").decode("ascii")
    result = create_commited_bit(secret, 5, key)
    assert result is not None
    commitment, bit, timestamp = result

    assert verify_bit(commitment, bit, timestamp, secret, key)
    assert not verify_bit(commitment, bit ^ 1, timestamp, secret, key)
    other_key = Key(ChaCha20Poly1305.generate_key(), 1, 1, 10)
    assert not verify_bit(commitment, bit, timestamp, secret, other_key)
