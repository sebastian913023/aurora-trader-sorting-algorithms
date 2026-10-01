"""Opportunity ranking, reusing the repo's sorting theme (top-N via heap)."""

from __future__ import annotations

import heapq
from collections.abc import Iterable

from .models import Opportunity


def _key(o: Opportunity) -> tuple[float, str, str]:
    # Highest edge first; ties broken deterministically by market id then side.
    return (o.edge, o.market_id, o.side.value)


def rank_opportunities(opps: Iterable[Opportunity], limit: int | None = None) -> list[Opportunity]:
    """Descending by net edge with a total-order tiebreak (deterministic)."""
    items = list(opps)
    if limit is None:
        return sorted(items, key=lambda o: (-o.edge, o.market_id, o.side.value))
    # nlargest is O(n log k); negate id ordering via a second pass for ties.
    top = heapq.nlargest(limit, items, key=lambda o: (o.edge, _neg(o.market_id), _neg(o.side.value)))
    return top


class _neg(str):
    """String wrapper that reverses ordering, so ids ascend inside nlargest."""

    def __lt__(self, other: str) -> bool:  # type: ignore[override]
        return str.__gt__(self, other)

    def __gt__(self, other: str) -> bool:  # type: ignore[override]
        return str.__lt__(self, other)
