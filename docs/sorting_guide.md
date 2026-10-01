# docs/sorting_guide.md

# Sorting Guide for Aurora Trader

Sorting is the process of arranging a collection of values into an order that is easier to search, compare, or process.

## Why sorting matters

In everyday programming, sorting helps us:

- display data in a useful order
- rank information by priority
- simplify search and comparison logic
- organize market data
- optimize downstream algorithms

In Aurora Trader, sorting is essential for:

- matching bids and asks
- ranking trading signals
- evaluating portfolio performance
- handling executions in order

## Fundamental concepts

### Stable sort
A stable sort keeps items with equal keys in their original relative order.

### In-place sort
A sort is in-place if it uses only a small additional memory footprint and rearranges the original collection.

### Time complexity
This describes how execution time grows as input size grows.

## Core algorithms

### Bubble sort
Bubble sort repeatedly swaps adjacent out-of-order elements.

- Good for teaching
- Slow for large datasets
- Best case: O(n)
- Average/worst: O(n^2)

### Selection sort
Selection sort repeatedly finds the next smallest item and places it correctly.

- Simple and predictable
- O(n^2) in all cases

### Insertion sort
Insertion sort builds a sorted prefix by inserting each new item into the correct location.

- Great for small or nearly sorted arrays
- Efficient for partially ordered data
- Best case: O(n)

### Merge sort
Merge sort divides and conquers by recursively sorting halves and merging them.

- Reliable and predictable
- Stable
- O(n log n)
- More memory than in-place sorts

### Quick sort
Quick sort partitions data around a pivot, recursively sorting the partitions.

- Fast average case
- Worst case can degrade to O(n^2)
- Great general-purpose choice in many systems

### Heap sort
Heap sort uses a binary heap to repeatedly extract the largest or smallest value.

- O(n log n)
- Good for memory-aware sorting

### Counting sort
Counting sort is ideal when the key range is limited and values are integers.

- Often O(n + k)
- Not general for arbitrary comparable values

### Radix sort
Radix sort sorts by digits or bytes rather than direct comparisons.

- Excellent for fixed-width integer data
- Great when the value range is manageable

### Bucket sort
Bucket sort partitions values across ranges and sorts each bucket.

- Good when values are distributed evenly
- Performance depends on bucket design

## Which one should I choose?

- Use Python's built-in sort for real code: `sorted()` or `.sort()`
- Use insertion sort for tiny or nearly sorted data
- Use merge sort when predictability and stability matter
- Use quick sort when general speed is important
- Use counting/radix/bucket sort when the data structure is suitable

## Aurora Trader connection

In a trading system, sorting is used to:

- prioritize bids vs asks
- rank signals by confidence
- rank positions by performance
- decide which trade to execute first

Sorting is operationally important, not simply theoretical.
