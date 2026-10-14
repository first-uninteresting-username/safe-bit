from fastapi import FastAPI

from .create_bit_verify import create_commited_bit
from .key_store import KeyStore
from .variables import DB_PATH
from .verify_requests import NewBitRequest, verify_get_bit

app = FastAPI()


@app.get("/health", summary="Check service health")
def health() -> dict[str, str]:
    """Check whether the API is running.

    Returns a status of `ok` when the service can handle requests.
    """
    return {"status": "ok"}


@app.post("/new-bit", summary="Create a new bit")
async def new_bit(req: NewBitRequest) -> dict[str, str | int]:
    store = KeyStore(DB_PATH)
    timestamp = verify_get_bit(req)
    key = store.ensure_current_key(timestamp, True)
    result = create_commited_bit(req.secret, timestamp, key)
    commitment, bit, _ = result
    return {
        "commitment": commitment,
        "bit": bit,
        "timestamp": timestamp,
        "secret": req.secret,
    }


# @app.get("/new-bit-generate-secret", )
