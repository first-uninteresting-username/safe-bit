from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


class key:
    def __init__(self, generation: int):
        self.material: bytes = ChaCha20Poly1305.generate_key()
        self.cipher: ChaCha20Poly1305 = ChaCha20Poly1305(self.material)
        self.generation: int = generation

    def encrypt_minute(self, minute: int) -> bytes:
        nonce = self.generation.to_bytes(4, "big") + minute.to_bytes(8, "big")
        encrypted = self.cipher.encrypt(nonce, minute.to_bytes(), None)
        return encrypted
