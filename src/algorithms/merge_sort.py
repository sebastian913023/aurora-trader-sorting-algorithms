"""Merge sort implementation."""

from __future__ import annotations


def merge_sort(values: list[int]) -> list[int]:
    """Return a sorted list using merge sort.

    Merge sort uses divide-and-conquer: it splits the list, recursively sorts each
    half, and then merges the two sorted halves back together.

    Time complexity:
        O(n log n)

    Space complexity:
        O(n)
    """
    arr = list(values)
    if len(arr) <= 1:
        return arr

    middle = len(arr) // 2
    left = merge_sort(arr[:middle])
    right = merge_sort(arr[middle:])

    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    merged: list[int] = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
