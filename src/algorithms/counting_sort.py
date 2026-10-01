"""Counting sort implementation."""

from __future__ import annotations


def counting_sort(values: list[int]) -> list[int]:
    """Return a sorted list using counting sort.

    Counting sort is efficient when the range of values is relatively small.

    Time complexity:
        O(n + k)

    Space complexity:
        O(k)

    where k is the range of input values.
    """
    arr = list(values)
    if not arr:
        return []

    minimum = min(arr)
    maximum = max(arr)
    counts = [0] * (maximum - minimum + 1)

    for value in arr:
        counts[value - minimum] += 1

    output: list[int] = []
    for index, count in enumerate(counts):
        output.extend([index + minimum] * count)

    return output
