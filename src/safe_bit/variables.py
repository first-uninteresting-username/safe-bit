from datetime import UTC, datetime
from os import environ
from pathlib import Path

# Everything will be configurable in the future

# Default length of generated secret
SECRET_LENGTH = int(environ.get("SECRET_LENGTH", "32"))
# datetime from which time is counted
# Sep 14 2026 00:00:00 UTC
# 1789344000
_t0 = datetime.fromisoformat(environ.get("T0", "2026-09-14T00:00:00+00:00"))
if _t0.utcoffset() is None:
    raise ValueError("T0 must be an ISO timestamp with a timezone")
T0 = _t0.astimezone(UTC)
# How long keys are valid for (in minutes)
# Week
KEY_VALIDITY = int(environ.get("KEY_VALIDITY", "10080"))
# Default location of the sqlite database for keys
DB_PATH = Path(environ.get("DB_PATH", "/var/lib/safe-bit/app.sqlite3"))
# How much drift between server time and user declared time is allowed
ALLOWED_DRIFT = int(environ.get("ALLOWED_DRIFT", "5"))
