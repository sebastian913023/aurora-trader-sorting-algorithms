"""Insertion sort implementation."""

from __future__ import annotations


def insertion_sort(values: list[int]) -> list[int]:
    """Return a sorted list using insertion sort.

    Insertion sort grows a sorted prefix by inserting each next item into the
    correct position among the earlier items.

    Time complexity:
        Best: O(n)
        Average: O(n^2)
        Worst: O(n^2)

    Space complexity:
        O(1)
    """
    arr = list(values)

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr
