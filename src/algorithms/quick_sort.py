"""Quick sort implementation."""

from __future__ import annotations


def quick_sort(values: list[int]) -> list[int]:
    """Return a sorted list using quick sort.

    Quick sort selects a pivot and partitions the list into elements smaller than
    and larger than the pivot, then recursively sorts the partitions.

    Time complexity:
        Average: O(n log n)
        Worst: O(n^2)

    Space complexity:
        Average: O(log n)
    """
    arr = list(values)
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    smaller = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    larger = [x for x in arr if x > pivot]

    return quick_sort(smaller) + equal + quick_sort(larger)
