from base64 import b64encode
from secrets import token_bytes

from .constants import SECRET_LENGTH
from .reimplementations.base64 import encode


def generate_secret(n: int = SECRET_LENGTH) -> bytes:
    return token_bytes(n)


def generate_secret_b64(n: int = SECRET_LENGTH) -> str:
    b = generate_secret(n)
    return encode(b)

def standard_generate_secret_b64(n: int = SECRET_LENGTH) -> str:
    b = generate_secret(n)
    return b64encode(b).decode("ascii")
