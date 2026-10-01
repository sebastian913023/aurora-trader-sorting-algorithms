"""Forecast-quality and sample-size statistics."""

from __future__ import annotations

import math
from collections.abc import Sequence


def brier_score(probs: Sequence[float], outcomes: Sequence[int]) -> float:
    """Mean squared error of probabilities vs 0/1 outcomes (lower is better)."""
    if len(probs) != len(outcomes) or not probs:
        raise ValueError("need equal-length, non-empty sequences")
    return sum((p - o) ** 2 for p, o in zip(probs, outcomes)) / len(probs)


def log_loss(probs: Sequence[float], outcomes: Sequence[int]) -> float:
    if len(probs) != len(outcomes) or not probs:
        raise ValueError("need equal-length, non-empty sequences")
    total = 0.0
    for p, o in zip(probs, outcomes):
        p = min(max(p, 1e-9), 1 - 1e-9)
        total -= o * math.log(p) + (1 - o) * math.log(1 - p)
    return total / len(probs)


def wilson_interval(wins: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a win rate."""
    if n <= 0 or not 0 <= wins <= n:
        raise ValueError("invalid wins/n")
    phat = wins / n
    denom = 1 + z * z / n
    centre = (phat + z * z / (2 * n)) / denom
    half = z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / denom
    return centre - half, centre + half
