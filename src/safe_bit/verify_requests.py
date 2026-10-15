from base64 import b64decode
from binascii import Error as Base64Error
from re import fullmatch
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from .variables import ALLOWED_DRIFT

Timestamp = Annotated[int, Field(strict=True, ge=0, le=2**63 - 1)]


class NewBitRequest(BaseModel):
    secret: str
    timestamp: Timestamp | None = None


class TimestampRequest(BaseModel):
    timestamp: Timestamp


class VerifyRequest(TimestampRequest):
    secret: str
    commitment: str
    bit: Annotated[int, Field(strict=True, ge=0, le=1)]

    @field_validator("commitment")
    @classmethod
    def validate_commitment(cls, value: str) -> str:
        verify_valid_b64(value)
        if len(b64decode(value, validate=True)) != 64:
            raise ValueError("Commitment must contain exactly 64 bytes")
        return value


class IsoRequest(BaseModel):
    iso: str


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
    except (Base64Error, ValueError) as e:
        raise NotBase64EncodedError(e)
    return


def verify_get_bit(
    request: NewBitRequest, now: int, allowed_diff: int = ALLOWED_DRIFT
) -> int:
    declared_time = request.timestamp if request.timestamp is not None else now

    time_diff = now - declared_time
    if time_diff > allowed_diff:
        raise DeclaredTimeInPastError(
            f"Declared time ({declared_time}) is {time_diff} minutes ago. Maximal allowed difference is {allowed_diff}"
        )
    if time_diff < 0:
        raise DeclaredTimeInFutureError(
            f"Declared time ({declared_time}) is in the future!"
        )

    # NotBase64EncodedError is raised by itself
    _ = verify_valid_b64(request.secret)

    return declared_time
