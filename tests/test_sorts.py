"""Tests for the sorting algorithms."""

from __future__ import annotations

import pytest

from src.algorithms.bubble_sort import bubble_sort
from src.algorithms.bucket_sort import bucket_sort
from src.algorithms.counting_sort import counting_sort
from src.algorithms.heap_sort import heap_sort
from src.algorithms.insertion_sort import insertion_sort
from src.algorithms.merge_sort import merge_sort
from src.algorithms.quick_sort import quick_sort
from src.algorithms.radix_sort import radix_sort
from src.algorithms.selection_sort import selection_sort


SORTING_ALGORITHMS = [
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
    counting_sort,
    bucket_sort,
    radix_sort,
]


def test_basic_sorted_output():
    data = [9, 3, 7, 1, 8, 2]
    expected = [1, 2, 3, 7, 8, 9]

    for sort_func in SORTING_ALGORITHMS:
        result = sort_func(data)
        assert result == expected


def test_empty_list():
    for sort_func in SORTING_ALGORITHMS:
        assert sort_func([]) == []


def test_single_item():
    for sort_func in SORTING_ALGORITHMS:
        assert sort_func([42]) == [42]


def test_duplicates():
    data = [4, 2, 2, 3, 1, 4]
    expected = [1, 2, 2, 3, 4, 4]

    for sort_func in SORTING_ALGORITHMS:
        assert sort_func(data) == expected


def test_reverse_sorted_input():
    data = [10, 9, 8, 7, 6, 5]
    expected = [5, 6, 7, 8, 9, 10]

    for sort_func in SORTING_ALGORITHMS:
        assert sort_func(data) == expected


def test_nearly_sorted_input():
    data = [1, 2, 3, 5, 4, 6, 7, 8]
    expected = [1, 2, 3, 4, 5, 6, 7, 8]

    for sort_func in SORTING_ALGORITHMS:
        assert sort_func(data) == expected


def test_counting_sort_handles_negative_values_via_offset():
    assert counting_sort([3, -1, 2, -1]) == [-1, -1, 2, 3]


def test_radix_sort_rejects_negative_values():
    with pytest.raises(ValueError):
        radix_sort([-1, 2, 3])
