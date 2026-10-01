"""Selection sort implementation."""

from __future__ import annotations


def selection_sort(values: list[int]) -> list[int]:
    """Return a sorted list using selection sort.

    Selection sort repeatedly finds the minimum element in the unsorted portion of
    the list and places it at the front.

    Time complexity:
        O(n^2)

    Space complexity:
        O(1)
    """
    arr = list(values)
    n = len(arr)

    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr
