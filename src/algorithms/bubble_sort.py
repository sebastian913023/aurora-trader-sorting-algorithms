"""Bubble sort implementation."""

from __future__ import annotations


def bubble_sort(values: list[int]) -> list[int]:
    """Return a sorted list using bubble sort.

    Bubble sort repeatedly compares adjacent elements and swaps them if they are
    out of order. It is simple to understand and useful for educational purposes,
    but it is usually inefficient on large lists.

    Time complexity:
        Best: O(n)
        Average: O(n^2)
        Worst: O(n^2)

    Space complexity:
        O(1)
    """
    arr = list(values)
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

    return arr
