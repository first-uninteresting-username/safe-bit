from logging import ERROR, StreamHandler
from logging import basicConfig as loggerConfig
from os import environ
from sys import stderr as sys_stderr

from uvicorn import run as uvicorn_run

from .variables import DB_PATH


def main() -> None:
    host = environ.get("SAFE_BIT_HOST", "127.0.0.1")
    port = int(environ.get("SAFE_BIT_PORT", "8000"))

    if not 1 <= port <= 65535:
        raise ValueError("SAFE_BIT_PORT must be between 1 and 65535")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    loggerConfig(
        level=ERROR,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            StreamHandler(sys_stderr),
        ],
    )

    uvicorn_run(
        "safe_bit.api:app",
        host=host,
        port=port,
        access_log=False,
        log_level="error",
    )


if __name__ == "__main__":
    main()
