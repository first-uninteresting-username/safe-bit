from datetime import UTC, datetime

import pytest


@pytest.fixture
def t0_datetime():
    return datetime(2026, 9, 14, 0, 0, 0, tzinfo=UTC)
