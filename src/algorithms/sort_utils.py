"""Shared utilities for sorting algorithms and demos."""

from __future__ import annotations

from random import randint
from typing import Iterable, List


def is_sorted(values: Iterable[int], reverse: bool = False) -> bool:
    """Return True if the values are sorted in ascending or descending order."""
    seq = list(values)
    if len(seq) < 2:
        return True
    for i in range(len(seq) - 1):
        left = seq[i]
        right = seq[i + 1]
        if reverse:
            if left < right:
                return False
        else:
            if left > right:
                return False
    return True


def generate_random_list(size: int, low: int = 0, high: int = 100) -> List[int]:
    """Create a random list of integers for benchmarking or testing."""
    return [randint(low, high) for _ in range(size)]


def nearly_sorted_list(size: int, swaps: int = 5) -> List[int]:
    """Generate a mostly sorted list with a few out-of-place elements."""
    values = list(range(size))
    for _ in range(swaps):
        i = randint(0, size - 1)
        j = randint(0, size - 1)
        values[i], values[j] = values[j], values[i]
    return values
