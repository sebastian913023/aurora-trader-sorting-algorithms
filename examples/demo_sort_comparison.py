"""A simple demo comparing sort performance on a generated dataset."""

from __future__ import annotations

from src.algorithms.bubble_sort import bubble_sort
from src.algorithms.insertion_sort import insertion_sort
from src.algorithms.merge_sort import merge_sort
from src.algorithms.quick_sort import quick_sort
from src.algorithms.selection_sort import selection_sort
from src.algorithms.sort_utils import generate_random_list


def main() -> None:
    data = generate_random_list(20, 0, 50)
    algorithms = {
        "bubble": bubble_sort,
        "selection": selection_sort,
        "insertion": insertion_sort,
        "merge": merge_sort,
        "quick": quick_sort,
    }

    print("Original data:", data)
    print()
    for name, func in algorithms.items():
        print(f"{name}: {func(data)}")


if __name__ == "__main__":
    main()
