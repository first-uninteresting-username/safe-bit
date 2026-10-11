from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


class key:
    def __init__(self, material: bytes, generation: int, valid_from: int, valid_until: int):
        if len(material) != 32:
            raise ValueError("Key material must be 32 bytes long")
        if generation <= 0:
            raise ValueError("Generation must be non negative")
        if valid_from <= 0:
            raise ValueError("Valid from must be non negative")
        if valid_until < 0:
            raise ValueError("Valid until must be positive")
        if valid_from > valid_until:
            raise ValueError("Valid from must be less than valid until")
        if generation >= 2**32:
            raise ValueError("Generation must be less than 2^32")

        self.material: bytes = material
        self.generation: int = generation
        self.valid_from: int = valid_from
        self.valid_until: int = valid_until

    def encrypt_minute(self, minute: int) -> bytes:
        cipher: ChaCha20Poly1305 = ChaCha20Poly1305(self.material)
        nonce = self.generation.to_bytes(4, "big") + minute.to_bytes(8, "big")
        encrypted = cipher.encrypt(nonce, minute.to_bytes(16, "big"), None)
        return encrypted
