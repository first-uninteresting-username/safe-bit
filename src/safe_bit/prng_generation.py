from hashlib import sha512


def hash_two_strings(s1: str, s2: str) -> str:
    string = s1 + s2
    b = string.encode("utf-8")
    digest = sha512(b).hexdigest()
    return digest

#def generate_random_bit_sequence(secret: str, key: key) -> str:
