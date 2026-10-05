from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from .constants import KEY_VALIDITY
from .time import get_current_time


class key:
    def __init__(self, generation: int):
        self.material: bytes = ChaCha20Poly1305.generate_key()
        self.cipher: ChaCha20Poly1305 = ChaCha20Poly1305(self.material)
        self.generation: int = generation
        self.valid_from: int = get_current_time()
        self.valid_until: int = self.valid_from + KEY_VALIDITY

    def encrypt_minute(self, minute: int) -> bytes:
        nonce = self.generation.to_bytes(4, "big") + minute.to_bytes(8, "big")
        encrypted = self.cipher.encrypt(nonce, minute.to_bytes(), None)
        return encrypted
