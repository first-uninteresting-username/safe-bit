from base64 import b64encode
from secrets import token_bytes


def generate_secret(n: int = 32) -> bytes:
    return token_bytes(n)


def generate_secret_b64(n: int = 32) -> str:
    b = generate_secret(n)
    return b64encode(b).decode("ascii")
