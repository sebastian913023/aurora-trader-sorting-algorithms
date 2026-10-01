"""Heap sort implementation."""

from __future__ import annotations


def heap_sort(values: list[int]) -> list[int]:
    """Return a sorted list using heap sort.

    Heap sort uses a binary heap data structure to repeatedly extract the
    smallest or largest element.

    Time complexity:
        O(n log n)

    Space complexity:
        O(1)
    """
    arr = list(values)
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _heapify(arr, end, 0)

    return arr


def _heapify(arr: list[int], size: int, root: int) -> None:
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < size and arr[left] > arr[largest]:
        largest = left
    if right < size and arr[right] > arr[largest]:
        largest = right
    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        _heapify(arr, size, largest)
