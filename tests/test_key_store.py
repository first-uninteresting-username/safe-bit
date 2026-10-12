from pathlib import Path

from safe_bit.key import Key
from safe_bit.key_store import KeyStore


def test_key_persists_after_closing_and_reopening(tmp_path: Path):
    db_path = tmp_path / "keys.db"
    minute = 12345
    store = KeyStore(db_path)
    try:
        key = store.generate_key_and_insert(minute)
        original_ciphertext = key.encrypt_minute(minute)
    finally:
        store.close()

    reopened = KeyStore(db_path)
    try:
        restored = reopened.get_key_for_minute(minute)
        assert restored.material == key.material
        assert restored.generation == key.generation
        assert restored.valid_from == key.valid_from
        assert restored.valid_until == key.valid_until
        assert restored.release_date == key.release_date
        assert restored.encrypt_minute(minute) == original_ciphertext
    finally:
        reopened.close()


def test_stored_release_date_is_preserved(tmp_path: Path):
    db_path = tmp_path / "keys.db"
    key = Key(bytes(32), 1, 10, 20, release_date=100)
    store = KeyStore(db_path)
    try:
        store.insert(key)
    finally:
        store.close()

    reopened = KeyStore(db_path)
    try:
        assert reopened.get_key_for_minute(10).release_date == 100
    finally:
        reopened.close()
