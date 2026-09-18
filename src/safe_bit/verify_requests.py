from base64 import b64decode
from re import fullmatch

from .time import get_current_time


class DeclaredTimeInPastError(ValueError):
    pass

class DeclaredTimeInFutureError(ValueError):
    pass

class NoSecretFieldError(ValueError):
    pass

class NotBase64EncodedError(ValueError):
    pass

def verify_valid_b64(s: str) -> None:
    if s == "":
        return
    if not fullmatch(r"^[A-Za-z0-9+/]*={0,2}$", s):
        raise NotBase64EncodedError(f"String {s} doesn't match Base64 regex")
    if len(s) % 4 != 0:
        raise NotBase64EncodedError(f"Length of string {s} isn't divisible by 4")
    try:
        _ = b64decode(s, validate=True)
    except Exception as e:  # noqa: BLE001 - fail on any error
        raise NotBase64EncodedError(e)
    return

# Todo: Switch to Pydantic model when you implement it in fastapi
def verify_get_bit(request: dict[str, str], allowed_diff: int = 5) -> int:
    time = get_current_time()
    if "secret" not in request:
            raise NoSecretFieldError("request is missing required 'secret' field")

    if "time" not in request:
        declared_time = time
    else:
        declared_time = int(request["time"])

    time_diff = time - declared_time
    if time_diff > allowed_diff:
        raise DeclaredTimeInPastError(f"Declared time ({declared_time}) is {time_diff} minutes ago. Maximal allowed difference is {allowed_diff}")
    if time_diff < 0:
        raise DeclaredTimeInFutureError(f"Declared time ({declared_time}) is in the future")

    # NotBase64EncodedError is raised by itself
    _ = verify_valid_b64(request["secret"])

    return declared_time
