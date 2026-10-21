from pathlib import Path
from sqlite3 import Connection, connect
from typing import cast

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from .key import Key
from .time import get_current_time
from .variables import KEY_VALIDITY


class NoKeyForMinuteError(ValueError):
    pass

class OverlappingKeyRangesError(ValueError):
    pass

class KeyStore:
    def __init__(self, db_path: Path):
        self._conn: Connection = connect(db_path, autocommit=True)
        _ = self._conn.execute("""
                CREATE TABLE IF NOT EXISTS keys (
                    generation   INTEGER PRIMARY KEY
                                 CHECK (generation >= 0 AND generation < 4294967296),
                    key_material BLOB NOT NULL
                                 CHECK (length(key_material) = 32),
                    valid_from   INTEGER NOT NULL CHECK (valid_from >= 0),
                     valid_until  INTEGER NOT NULL,
                    CHECK (valid_until > valid_from)
                );
            """)
        # Keep existing archives usable after removing the release-date field.
        columns = self._conn.execute("PRAGMA table_info(keys)").fetchall()
        if any(column[1] == "release_date" for column in columns):
            _ = self._conn.execute("ALTER TABLE keys DROP COLUMN release_date")

    def get_key_for_minute(self, minute: int) -> Key:
        if minute < 0 or minute >= 2**64:
            raise ValueError(f"Minute {minute} is out of range")

        rows = cast(
            list[tuple[bytes, int, int, int]],
            self._conn.execute(
                """
                SELECT key_material, generation, valid_from, valid_until
                FROM keys
                WHERE valid_from <= ? AND valid_until > ?
                LIMIT 2;
                """,
                (minute, minute),
            ).fetchall(),
        )

        if not rows:
            raise NoKeyForMinuteError(f"No key found for minute {minute}")

        if len(rows) > 1:
            raise OverlappingKeyRangesError(
                f"Multiple keys have overlapping validity ranges at minute {minute}"
            )

        key_material, generation, valid_from, valid_until = rows[0]
        return Key(key_material, generation, valid_from, valid_until)

    def insert(self, key: Key) -> None:

        owns_transaction = not self._conn.in_transaction
        if owns_transaction:
            _ = self._conn.execute("BEGIN IMMEDIATE")
        try:
            overlap = cast(
                tuple[int] | None,
                self._conn.execute(
                    """
                    SELECT 1 FROM keys
                    WHERE valid_from < ? AND ? < valid_until
                    LIMIT 1;
                    """,
                    (key.valid_until, key.valid_from),
                ).fetchone(),
            )

            if overlap is not None:
                raise OverlappingKeyRangesError("Key overlaps with existing key")

            _ = self._conn.execute(
                """
                INSERT INTO keys
                    (generation, key_material, valid_from, valid_until)
                VALUES (?, ?, ?, ?);
                """,
                (
                    key.generation,
                    key.material,
                    key.valid_from,
                    key.valid_until,
                ),
            )
            if owns_transaction:
                _ = self._conn.execute("COMMIT")
        except Exception:
            if owns_transaction:
                _ = self._conn.execute("ROLLBACK")
            raise

    def generate_key_and_insert(self, time: int | None = None) -> Key:
        if time is None:
                time = get_current_time()
        row = cast(
            tuple[int],
            self._conn.execute("""
            SELECT COALESCE(MAX(generation), 0) FROM keys
        """).fetchone(),
        )
        max_generation = row[0]

        generation = max_generation + 1
        material = ChaCha20Poly1305.generate_key()
        valid_from = time
        valid_until = valid_from + KEY_VALIDITY

        key = Key(material, generation, valid_from, valid_until)
        self.insert(key)
        return key

    def ensure_current_key(self, time: int | None = None, allow_creation: bool = True) -> Key:
        if time is None:
                time = get_current_time()
        _ = self._conn.execute("BEGIN IMMEDIATE")
        try:
            minute = time
            try:
                key = self.get_key_for_minute(minute)
            except NoKeyForMinuteError:
                if allow_creation:
                    key = self.generate_key_and_insert(minute)
                else:
                    raise
            _ = self._conn.execute("COMMIT")
            return key
        except Exception:
            _ = self._conn.execute("ROLLBACK")
            raise

    def close(self) -> None:
        self._conn.close()
