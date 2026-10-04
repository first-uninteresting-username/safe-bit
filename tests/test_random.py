from collections.abc import Iterator

from safe_bit.random_generation import (
    _generate_byte_sequence,  # pyright: ignore[reportPrivateUsage]
)


def _generate_byte_sequence_reference(seed: int, count: int) -> Iterator[int]:
    """This function must not be changed"""
    s = seed
    for _ in range(count):
            s = (1664525 * s + 1013904223) % 4294967296
            yield s // 16777216

def test_random_bit_generation():
    """This test must not be changed"""
    for i in range(1000):
        assert list(_generate_byte_sequence(i, 16)) == list(
            _generate_byte_sequence_reference(i, 16)
        )
