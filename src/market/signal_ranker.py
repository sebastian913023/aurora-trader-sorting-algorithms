"""Signal ranking for Aurora Trader."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Signal:
    """A trading signal with a score and a name."""

    name: str
    score: float
    strength: str = "neutral"


class SignalRanker:
    """Rank signals according to importance or confidence."""

    @staticmethod
    def rank(signals: list[Signal]) -> list[Signal]:
        """Return signals sorted by descending score."""
        return sorted(signals, key=lambda signal: signal.score, reverse=True)

    @staticmethod
    def top_n(signals: list[Signal], limit: int) -> list[Signal]:
        """Return the strongest signals, capped at a limit."""
        return SignalRanker.rank(signals)[:limit]
