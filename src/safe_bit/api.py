import logging
from base64 import b64encode
from datetime import datetime
from hashlib import sha512
from pathlib import Path
from sqlite3 import Error

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .create_bit_verify import create_commited_bit, verify_bit_checks
from .frontend import router as frontend_router
from .key import Key
from .key_store import KeyStore, NoKeyForMinuteError, OverlappingKeyRangesError
from .secret import generate_secret
from .time import get_current_time, get_date_from_time, get_time
from .variables import ALLOWED_DRIFT, DB_PATH, KEY_VALIDITY, RELEASE_DELAY, T0
from .verify_requests import (
    DeclaredTimeInFutureError,
    DeclaredTimeInPastError,
    IsoRequest,
    NewBitRequest,
    NotBase64EncodedError,
    TimestampRequest,
    VerifyRequest,
    verify_get_bit,
    verify_valid_b64,
)

app = FastAPI()
app.include_router(frontend_router)
logger = logging.getLogger(__name__)


def _get_key(timestamp: int, *, allow_creation: bool = False) -> Key:
    try:
        store = KeyStore(DB_PATH)
        try:
            if allow_creation:
                return store.ensure_current_key(timestamp, True)
            return store.get_key_for_minute(timestamp)
        finally:
            store.close()
    except NoKeyForMinuteError as exc:
        raise HTTPException(404, "No archived key for this timestamp.") from exc
    except OverlappingKeyRangesError as exc:
        logger.exception("Overlapping key ranges")
        raise HTTPException(500, "Overlapping key ranges.") from exc
    except Error as exc:
        logger.exception("Database operation failed")
        raise HTTPException(500, "Database operation failed.") from exc


def _validate_secret(secret: str) -> None:
    try:
        verify_valid_b64(secret)
    except NotBase64EncodedError as exc:
        raise HTTPException(400, "Secret must be valid Base64.") from exc


def _iso_for_timestamp(timestamp: int) -> str:
    try:
        return get_date_from_time(timestamp).isoformat()
    except OverflowError as exc:
        raise HTTPException(400, "Timestamp is outside the datetime range.") from exc

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).resolve().parent / "web/static"),
    name="static",
)

@app.get("/health", summary="Check service health")
def health() -> dict[str, str]:
    """Check whether the API is running.

    Returns a status of `ok` when the service can handle requests.
    """
    _ = _get_key(get_current_time(), allow_creation=True)
    return {"status": "ok"}


@app.post("/new-bit", summary="Create a new bit")
def new_bit(req: NewBitRequest) -> dict[str, str | int]:
    """Get a new bit with b64 encoded secret.

    Returns commitment, bit and timestamp.
    """
    now = get_current_time()
    try:
        timestamp = verify_get_bit(req, now)
    except DeclaredTimeInPastError as exc:
        raise HTTPException(
            400, f"Timestamp must be at most {ALLOWED_DRIFT} minutes in the past."
        ) from exc
    except DeclaredTimeInFutureError as exc:
        raise HTTPException(400, "Timestamp must not be in the future.") from exc
    except NotBase64EncodedError as exc:
        raise HTTPException(400, "Secret must be valid Base64.") from exc

    key = _get_key(timestamp, allow_creation=True)
    commitment, bit, _ = create_commited_bit(req.secret, timestamp, key)
    return {"commitment": commitment, "bit": bit, "timestamp": timestamp}


@app.post("/release", summary="Release a locked minute after the delay")
def release(req: TimestampRequest) -> JSONResponse:
    """Release b64 encoded locked minute.

    The locked minute is available at or after its key's stored release date.

    Returns timestamp, locked minute and number of key generation
    """
    key = _get_key(req.timestamp)
    available = key.release_date
    if get_current_time() < available:
        return JSONResponse(
            status_code=425,
            content={"locked": True, "available_at": _iso_for_timestamp(available)},
        )
    return JSONResponse(
        content={
            "timestamp": req.timestamp,
            "locked_minute": b64encode(key.encrypt_minute(req.timestamp)).decode(
                "ascii"
            ),
            "key_generation": key.generation,
        }
    )


@app.post("/verify", summary="Verify a committed bit using the key archive")
def verify(req: VerifyRequest) -> dict[str, bool | dict[str, bool]]:
    """Verify a committed bit using the archived key for its timestamp.

    Returns the individual checks and whether all checks passed.
    """
    _validate_secret(req.secret)
    key = _get_key(req.timestamp)
    checks = verify_bit_checks(req.commitment, req.bit, req.timestamp, req.secret, key)
    return {"valid": all(checks.values()), "checks": checks}


@app.post("/time-for-iso", summary="Convert an ISO 8601 datetime to server time")
async def time_for_iso(req: IsoRequest) -> dict[str, int]:
    """Convert a timezone-aware ISO 8601 datetime to server minutes since T₀.

    Returns the timestamp rounded down to a whole minute. Raise HTTP 400 for
    invalid datetimes, missing timezones, or timestamps before T₀.
    """
    try:
        date = datetime.fromisoformat(req.iso)
        if date.utcoffset() is None:
            raise ValueError("A timezone is required")
        timestamp = get_time(date)
        if timestamp < 0:
            raise ValueError("Datetime precedes the reference date")
    except (ValueError, OverflowError) as exc:
        raise HTTPException(
            400, "Expected a timezone-aware datetime on or after T₀."
        ) from exc
    return {"timestamp": timestamp}


@app.post("/iso-for-time", summary="Convert server time to an ISO 8601 datetime")
async def iso_for_time(req: TimestampRequest) -> dict[str, str]:
    """Return the ISO 8601 datetime for a server timestamp in minutes since T₀.

    Raise HTTP 400 if the timestamp is outside the supported datetime range.
    """
    return {"iso": _iso_for_timestamp(req.timestamp)}

@app.get("/info", summary="Return server information")
async def info() -> JSONResponse:
    """Return the server's reference date and relase/validity period."""
    return JSONResponse(
        content={
            "reference-date": T0.isoformat(),
            "key-validity": KEY_VALIDITY,
            "release-delay": RELEASE_DELAY,
        }
    )

@app.get("/secret", summary="Create a secret")
def secret() -> JSONResponse:
    """Generate a secret ready to be used in the /get-bit endpoint.

    Returns secret as b64 string, sha512 of the secret bytes and sha512 of the b64 string.
    """
    secret = generate_secret()
    secret_b64 = b64encode(secret).decode("ascii")
    sha512_secret = sha512(secret).hexdigest()
    sha512_secret_b64 = sha512(secret_b64.encode("ascii")).hexdigest()
    return JSONResponse(
        content={
            "secret-b64": secret_b64,
            "sha512-secret": sha512_secret,
            "sha512-secret-b64": sha512_secret_b64,
        }
    )
