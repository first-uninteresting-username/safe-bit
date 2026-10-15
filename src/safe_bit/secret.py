from secrets import token_bytes

from .variables import SECRET_LENGTH


def generate_secret(n: int = SECRET_LENGTH) -> bytes:
    return token_bytes(n)
