"""Paper broker: simulated fills at the ask, with fees. Never touches the network."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import Decision, Side


@dataclass
class Position:
    market_id: str
    side: Side
    shares: float
    cost: float  # USD paid including fee


@dataclass
class PaperBroker:
    cash: float
    positions: list[Position] = field(default_factory=list)
    realized_pnl: float = 0.0

    @property
    def exposure(self) -> float:
        return sum(p.cost for p in self.positions)

    @property
    def equity_at_cost(self) -> float:
        return self.cash + self.exposure

    def execute(self, decision: Decision) -> Position | None:
        """Fill an approved decision. stake = total USD incl. fee."""
        if not decision.approved or decision.stake <= 0 or decision.stake > self.cash:
            return None
        opp = decision.opportunity
        shares = decision.stake / (opp.price + opp.fee_per_share)
        pos = Position(opp.market_id, opp.side, shares, decision.stake)
        self.cash -= decision.stake
        self.positions.append(pos)
        return pos

    def settle(self, market_id: str, yes_won: bool) -> float:
        """Settle all positions in a market; returns realized PnL."""
        pnl = 0.0
        remaining = []
        for pos in self.positions:
            if pos.market_id != market_id:
                remaining.append(pos)
                continue
            won = (pos.side is Side.YES) == yes_won
            payout = pos.shares if won else 0.0
            self.cash += payout
            pnl += payout - pos.cost
        self.positions = remaining
        self.realized_pnl += pnl
        return pnl
