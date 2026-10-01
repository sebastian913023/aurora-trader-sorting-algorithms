"""Benchmark tools for comparing sorting algorithms."""

from __future__ import annotations

import time
from typing import Callable, Iterable

from src.algorithms.bubble_sort import bubble_sort
from src.algorithms.bucket_sort import bucket_sort
from src.algorithms.counting_sort import counting_sort
from src.algorithms.heap_sort import heap_sort
from src.algorithms.insertion_sort import insertion_sort
from src.algorithms.merge_sort import merge_sort
from src.algorithms.quick_sort import quick_sort
from src.algorithms.radix_sort import radix_sort
from src.algorithms.selection_sort import selection_sort


def benchmark_algorithm(name: str, func: Callable[[list[int]], list[int]], values: list[int]) -> tuple[str, float]:
    """Run one sort function and return its name and elapsed time."""
    start = time.perf_counter()
    result = func(values)
    elapsed = time.perf_counter() - start
    _ = result
    return name, elapsed


def benchmark_suite(values: list[int]) -> dict[str, float]:
    """Run a suite of algorithm comparisons and return timing data."""
    algorithms: dict[str, Callable[[list[int]], list[int]]] = {
        "bubble": bubble_sort,
        "selection": selection_sort,
        "insertion": insertion_sort,
        "merge": merge_sort,
        "quick": quick_sort,
        "heap": heap_sort,
        "counting": counting_sort,
        "bucket": bucket_sort,
        "radix": radix_sort,
    }

    results: dict[str, float] = {}
    for name, func in algorithms.items():
        results[name] = benchmark_algorithm(name, func, values)[1]
    return results


def print_benchmark_report(values: Iterable[int]) -> None:
    """Pretty-print a benchmark comparison for the current data set."""
    item_list = list(values)
    results = benchmark_suite(item_list)

    print("Sorting benchmark results")
    print("=" * 30)
    for name, elapsed in results.items():
        print(f"{name:10s}: {elapsed:.6f}s")
