"""Bucket sort implementation."""

from __future__ import annotations


def bucket_sort(values: list[int]) -> list[int]:
    """Return a sorted list using bucket sort.

    Bucket sort distributes values into buckets based on their range, sorts each
    bucket, and concatenates them.

    Time complexity:
        Average: O(n + k)
        Worst: O(n^2)

    where k is the number of buckets.
    """
    arr = list(values)
    if not arr:
        return []

    minimum = min(arr)
    maximum = max(arr)
    bucket_count = max(1, len(arr))
    buckets: list[list[int]] = [[] for _ in range(bucket_count)]

    if maximum == minimum:
        return arr

    for value in arr:
        index = int((value - minimum) / (maximum - minimum + 1) * bucket_count)
        index = min(index, bucket_count - 1)
        buckets[index].append(value)

    output: list[int] = []
    for bucket in buckets:
        bucket.sort()
        output.extend(bucket)

    return output
