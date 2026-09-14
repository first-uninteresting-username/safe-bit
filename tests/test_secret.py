from base64 import b64decode

from safe_bit.secret import generate_secret, generate_secret_b64


def test_generate_secret():
    l = 32
    secret = generate_secret(l)
    assert len(secret) == l
    assert type(secret) == bytes

def test_generate_secret_b64():
    l = 32
    secret_b64 = generate_secret_b64(l)
    secret = b64decode(secret_b64)
    assert len(secret) == l
    assert type(secret) == bytes
