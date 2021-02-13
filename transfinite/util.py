from typing import Any


def is_non_negative_int(n: Any) -> bool:
    """
    Return True if n is a non-negative integer.

    If n is a negative integer raise a ValueError, else return False.
    """
    if isinstance(n, int) and n >= 0:
        return True
    if isinstance(n, int):
        raise ValueError(f"int value must be non-negative (got {n})")
    return False
