from sqlite3 import Error

from fastapi import FastAPI, HTTPException

from .create_bit_verify import create_commited_bit
from .key_store import KeyStore, OverlappingKeyRangesError
from .time import get_current_time
from .variables import ALLOWED_DRIFT, DB_PATH
from .verify_requests import (
    DeclaredTimeInFutureError,
    DeclaredTimeInPastError,
    NewBitRequest,
    NotBase64EncodedError,
    verify_get_bit,
)

app = FastAPI()


@app.get("/health", summary="Check service health")
def health() -> dict[str, str]:
    """Check whether the API is running.

    Returns a status of `ok` when the service can handle requests.
    """
    return {"status": "ok"}


@app.post("/new-bit", summary="Create a new bit")
async def new_bit(req: NewBitRequest) -> dict[str, str | int]:
    now = get_current_time()
    try:
        timestamp = verify_get_bit(req, now)
    except DeclaredTimeInPastError:
        raise HTTPException(
            status_code=400,
            detail=f"Provided timestamp {req.timestamp} is more than {ALLOWED_DRIFT} minutes in the past. Current time is {now}.",
        )
    except DeclaredTimeInFutureError:
        raise HTTPException(
            status_code=400,
            detail=f"Provided timestamp {req.timestamp} is in the future. Current time is {now}."
        )
    except NotBase64EncodedError:
        raise HTTPException(
            status_code=400,
            detail=f"Provided secret {req.secret} is not base64 encoded."
        )

    try:
        store = KeyStore(DB_PATH)
        try:
            key = store.ensure_current_key(timestamp, True)
        finally:
            store.close()
    except OverlappingKeyRangesError:
        raise HTTPException(
            status_code=500,
            detail="Overlapping key ranges. This should never happen. Contact the entity managing this server."
        )
    except Error:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed.",
        )


    result = create_commited_bit(req.secret, timestamp, key)
    commitment, bit, _ = result
    return {
        "commitment": commitment,
        "bit": bit,
        "timestamp": timestamp,
        "secret": req.secret,
    }


# @app.get("/new-bit-generate-secret", )
