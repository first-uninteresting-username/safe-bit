from datetime import UTC, datetime
from pathlib import Path

# Everything will be configurable in the future

# Default length of generated secret
SECRET_LENGTH = 32
# datetime from which time is counted
# Sep 14 2026 00:00:00 UTC
# 1789344000
T0 = datetime(2026, 9, 14, 0, 0, 0, tzinfo=UTC)
# How long keys are valid for (in minutes)
# Week
KEY_VALIDITY = 10080
# How long to wait before releasing minutes encrypted with keys
# 4 times key validity
RELEASE_DELAY = KEY_VALIDITY * 4
# Default location of the sqlite database for keys
DB_PATH = Path("/var/lib/safe-bit/app.sqlite3")
# How much drift between server time and user declared time is allowed
ALLOWED_DRIFT = 5
