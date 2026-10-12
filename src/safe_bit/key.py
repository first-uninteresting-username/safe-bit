from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from .constants import RELEASE_DELAY


class Key:
    def __init__(
        self,
        material: bytes,
        generation: int,
        valid_from: int,
        valid_until: int,
        *,
        release_date: int | None = None,
    ):
        if len(material) != 32:
            raise ValueError("Key material must be 32 bytes long")
        if not 0 <= generation < 2**32:
                raise ValueError("Generation must fit an unsigned 32-bit integer")
        if not 0 <= valid_from < valid_until:
            raise ValueError("Validity must satisfy 0 <= valid_from < valid_until")
        if valid_from > valid_until:
            raise ValueError("Valid from must be less than valid until")
        if release_date is None:
            release_date = valid_until + RELEASE_DELAY
        if release_date < valid_until:
            raise ValueError("Release date must be at or after valid until")

        self.material: bytes = material
        self.generation: int = generation
        self.valid_from: int = valid_from
        self.valid_until: int = valid_until
        self.release_date: int = release_date


    def encrypt_minute(self, minute: int) -> bytes:
        cipher: ChaCha20Poly1305 = ChaCha20Poly1305(self.material)
        nonce = self.generation.to_bytes(4, "big") + minute.to_bytes(8, "big")
        encrypted = cipher.encrypt(nonce, minute.to_bytes(16, "big"), None)
        return encrypted

    def release_minute(self, minute: int) -> bytes:
        if minute > self.release_date:
            raise ValueError("Minute must be less than or equal to release date")
        return self.encrypt_minute(minute)
