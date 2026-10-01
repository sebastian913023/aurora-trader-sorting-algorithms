# CLAUDE.md

You are Claude Code working inside this repository. Build an ambitious, high-quality sorting algorithms learning project called Aurora Trader. This repo should be a polished educational lab with a trading simulation theme, not a bare coding exercise.

## Mission

Create a project that teaches sorting algorithms deeply, visually, and practically while also simulating a real trading platform. The repo should help learners move from basic awareness of `sorted()` to understanding algorithmic trade-offs, complexity, stability, and real-world coding decisions.

## Core concept

Aurora Trader is a simulated trading platform where order books, market data, signals, and portfolio rankings all rely on sorting. Sorting is not cosmetic here — it is decision-making infrastructure.

## Learning goals

- Teach bubble, selection, insertion, merge, quick, heap, counting, radix, and bucket sort.
- Explain time complexity and space complexity clearly.
- Compare stable vs unstable and in-place vs out-of-place algorithms.
- Show how sorting appears in real code and trading systems.
- Provide tests, exercises, and benchmarking scripts.
- Make the project feel visionary and polished.

## Repository structure

- `src/algorithms/` for algorithm implementations
- `src/market/` for trading simulation logic
- `src/analysis/` for benchmarks and comparison tools
- `example/` or `examples/` for runnable demos
- `tests/` for correctness and exploratory tests
- `docs/` for explanations and exercises
- `README.md` with a strong project overview

## Standards

- Use Python 3.11+
- Use type hints and docstrings
- Use pytest for tests
- Keep code readable and explicit
- Favor educational value over cleverness
- Add benchmark and exploratory reasoning where useful

## Implementation expectations

### Sorting algorithms

Implement the following:

- `bubble_sort`
- `selection_sort`
- `insertion_sort`
- `merge_sort`
- `quick_sort`
- `heap_sort`
- `counting_sort`
- `radix_sort`
- `bucket_sort`

Each function should:
- accept a list of integers or comparable values
- return a sorted list
- avoid mutating input unless explicitly documented
- include docstrings with complexity notes

### Aurora Trader logic

Add market logic around sorting:

- `OrderBook` sorts bids and asks by price
- `SignalRanker` sorts trading signals by confidence
- `Portfolio` or rankings can sort positions by performance
- `BenchmarkRunner` compares sorting performance

### Testing

Write tests that verify:
- Sorted output is correct
- Edge cases work
- Duplicates are handled correctly
- Reverse-sorted and nearly sorted inputs are handled
- Stable sorting is preserved where relevant

### Documentation

Add docs explaining:
- each algorithm
- why it matters
- complexity trade-offs
- when to choose a sort
- examples from trading logic

## Recommended files

- `README.md`
- `requirements.txt`
- `src/__init__.py`
- `src/algorithms/__init__.py`
- `src/market/__init__.py`
- `src/analysis/__init__.py`
- `src/algorithms/*.py`
- `src/market/order_book.py`
- `src/market/signal_ranker.py`
- `src/analysis/benchmark.py`
- `tests/test_sorts.py`
- `examples/demo_sort_comparison.py`
- `docs/sorting_guide.md`
- `docs/exercise_bank.md`

## Output quality bar

The project should feel polished, educational, and real. It should be the kind of repo a learner can explore from start to finish and genuinely understand.

When you build this repo, prioritize clarity, tests, quality explanations, and a coherent trading-themed narrative.
