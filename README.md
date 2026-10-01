# Aurora Trader: Sorting Algorithms Learning Lab

Aurora Trader is an immersive Python project for learning sorting algorithms through a simulated trading platform.

The project teaches the fundamentals of sorting while grounding them in real-world decision-making: order books, price ranking, signal prioritization, portfolio comparisons, and market analysis.

## Why this project exists

Sorting is one of the most important skills in software engineering. It shapes:

- decision-making speed
- search efficiency
- ranking systems
- market order processing
- analytics and dashboards
- performance-sensitive code

This repo turns sorting from an abstract topic into something practical and memorable.

## Algorithms covered

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Heap Sort
- Counting Sort
- Radix Sort
- Bucket Sort

## Core idea

In a trading platform:

- bids and asks must be sorted by price
- signals must be ranked by confidence
- positions may be ranked by risk or performance
- trade executions depend on ordering

Sorting is not just organization — it is a competitive advantage.

## Project layout

```text
aurora-trader-sorting-algorithms/
├── README.md
├── CLAUDE.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── bubble_sort.py
│   │   ├── selection_sort.py
│   │   ├── insertion_sort.py
│   │   ├── merge_sort.py
│   │   ├── quick_sort.py
│   │   ├── heap_sort.py
│   │   ├── counting_sort.py
│   │   ├── radix_sort.py
│   │   ├── bucket_sort.py
│   │   └── sort_utils.py
│   ├── market/
│   │   ├── __init__.py
│   │   ├── order_book.py
│   │   └── signal_ranker.py
│   └── analysis/
│       ├── __init__.py
│       └── benchmark.py
├── tests/
│   └── test_sorts.py
├── examples/
│   └── demo_sort_comparison.py
├── docs/
│   ├── sorting_guide.md
│   └── exercise_bank.md
└── benchmarks/
    └── compare_sorting_algorithms.py
```

## Getting started

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the tests

```bash
pytest
```

### 4. Run the demo

```bash
python examples/demo_sort_comparison.py
```

### 5. Run the benchmark

```bash
python benchmarks/compare_sorting_algorithms.py
```

## Quick example

```python
from src.algorithms.merge_sort import merge_sort

numbers = [9, 3, 7, 1, 8, 2]
print(merge_sort(numbers))
# [1, 2, 3, 7, 8, 9]
```

## Why sorting matters in code

Sorting helps with:

- displaying ranked results
- making search faster
- organizing data for visualizations
- matching trade orders
- processing logs and analytics
- determining the most important signals

## Learning path

1. Start with bubble, selection, and insertion sort.
2. Learn merge and quick sort.
3. Explore heap and counting sort.
4. Understand stability and complexity.
5. Connect sorting to market logic and trading systems.

## Educational philosophy

This repo aims to teach both the mechanical process of sorting and the judgment of when to choose one algorithm over another.

A great sorting solution is not just a correct one — it is the correct solution for the shape of the data and the priorities of the system.

## License

MIT
