"""Radix sort implementation."""

from __future__ import annotations


def radix_sort(values: list[int]) -> list[int]:
    """Return a sorted list using radix sort.

    Radix sort processes digits or bytes from least significant to most
    significant, usually with counting sort as the inner stable sort.

    Time complexity:
        O(d * (n + k))

    where d is the number of digits and k is the key range.
    """
    arr = list(values)
    if not arr:
        return []

    if min(arr) < 0:
        raise ValueError("radix_sort currently supports non-negative integers only")

    digits = max(arr).bit_length()
    exp = 1
    while exp <= 10 ** (digits - 1):
        arr = _counting_sort_by_exponent(arr, exp)
        exp *= 10
    return arr


def _counting_sort_by_exponent(values: list[int], exponent: int) -> list[int]:
    counts = [0] * 10
    output = [0] * len(values)

    for value in values:
        index = (value // exponent) % 10
        counts[index] += 1

    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]

    for value in reversed(values):
        index = (value // exponent) % 10
        counts[index] -= 1
        output[counts[index]] = value

    return output
