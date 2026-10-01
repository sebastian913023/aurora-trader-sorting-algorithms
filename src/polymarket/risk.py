"""Risk limits and veto logic."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskLimits:
    min_edge: float = 0.03  # net edge per $1 payout required
    min_liquidity: float = 500.0
    kelly_multiplier: float = 0.25
    max_position_frac: float = 0.05  # of bankroll per trade
    max_total_exposure_frac: float = 0.30
    max_daily_loss_frac: float = 0.05
    min_days_to_resolution: float = 0.0


class CircuitBreaker:
    """Halts trading after a daily loss limit or a manual kill switch."""

    def __init__(self, start_equity: float, limits: RiskLimits) -> None:
        self.start_equity = start_equity
        self.limits = limits
        self.killed = False

    def kill(self) -> None:
        self.killed = True

    def tripped(self, equity: float) -> bool:
        loss = (self.start_equity - equity) / self.start_equity
        return self.killed or loss >= self.limits.max_daily_loss_frac
