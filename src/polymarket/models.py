"""Core data types."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Side(str, Enum):
    """Which outcome token is bought."""

    YES = "YES"
    NO = "NO"


@dataclass(frozen=True)
class Market:
    """Top-of-book snapshot of a binary market. Prices are in (0, 1)."""

    market_id: str
    question: str
    yes_bid: float
    yes_ask: float
    category: str = "other"
    liquidity: float = 0.0  # USD depth near the touch
    days_to_resolution: float = 30.0

    def __post_init__(self) -> None:
        if not (0.0 < self.yes_bid <= self.yes_ask < 1.0):
            raise ValueError(f"invalid book for {self.market_id}: {self.yes_bid}/{self.yes_ask}")

    @property
    def no_ask(self) -> float:
        """Price to buy NO = 1 - best YES bid."""
        return 1.0 - self.yes_bid

    @property
    def mid(self) -> float:
        return (self.yes_bid + self.yes_ask) / 2.0


@dataclass(frozen=True)
class Opportunity:
    """A candidate trade with its net-of-fee edge."""

    market_id: str
    side: Side
    price: float  # cost per $1-payout share
    prob: float  # our probability that this side wins
    edge: float  # prob - price - fee_per_share
    fee_per_share: float


@dataclass(frozen=True)
class Decision:
    """A sized, risk-approved trade (or a veto with a reason)."""

    opportunity: Opportunity
    stake: float  # USD
    approved: bool
    reason: str = ""
