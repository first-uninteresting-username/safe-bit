from .base64_alphabet import ALPHABET


def _split_6bits(b: bytes) -> list[int]:
    value = int.from_bytes(b, byteorder='big')

    sections = [
        (value >> 18) & 0x3F,
        (value >> 12) & 0x3F,
        (value >> 6)  & 0x3F,
        value         & 0x3F,
    ]

    return sections


def encode(b: bytes) -> str:
    result = ""
    position = 0

    while position < len(b):
        byte1 = b[position:position + 1]

        if position + 1 < len(b):
            byte2 = b[position + 1:position + 2]
            have_b2 = True
        else:
            byte2 = b'\x00'
            have_b2 = False

        if position + 2 < len(b):
            byte3 = b[position + 2:position + 3]
            have_b3 = True
        else:
            byte3 = b'\x00'
            have_b3 = False

        full_bytes = byte1 + byte2 + byte3

        sections = _split_6bits(full_bytes)

        for i, section in enumerate(sections):
            if (i == 2 and not have_b2) or (i == 3 and not have_b3):
                result += "="
            else:
                result += ALPHABET[section]

        position = position + 3
    return result
