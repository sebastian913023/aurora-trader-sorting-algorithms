"""Benchmark runner for sort comparison."""

from __future__ import annotations

from src.analysis.benchmark import print_benchmark_report
from src.algorithms.sort_utils import generate_random_list


def main() -> None:
    values = generate_random_list(1000, 0, 500)
    print(f"Benchmarking on {len(values)} random values")
    print_benchmark_report(values)


if __name__ == "__main__":
    main()
