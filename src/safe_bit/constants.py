from datetime import UTC, datetime

# Default length of generated secret
SECRET_LENGTH = 32
# datetime from which time is counted
# Sep 14 2026 00:00:00 UTC
# 1789344000
T0 = datetime(2026, 9, 14, 0, 0, 0, tzinfo=UTC)
# For how long keys are valid (in minutes)
# Week
KEY_VALIDITY = 10080
