"""Orchestrates one persisted paper cycle. Paper only: no order is ever sent anywhere."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.polymarket.estimator import ProbabilityEstimator
from src.polymarket.models import Market
from src.polymarket.pipeline import run_cycle
from src.polymarket.risk import CircuitBreaker, RiskLimits

from .store import Store


def run_persisted_cycle(
    store: Store, markets: list[Market], estimator: ProbabilityEstimator, limits: RiskLimits | None = None, top_n: int = 10
) -> dict[str, Any]:
    limits = limits or RiskLimits()
    broker, state = store.load()
    today = datetime.now(timezone.utc).date()
    day_start = state["day_start_equity"]
    if str(state.get("day", today)) != str(today):  # new UTC day: reset the daily-loss baseline
        day_start = broker.equity_at_cost
        store._req("PATCH", "ae_state?id=eq.1", json={"day": str(today), "day_start_equity": day_start},
                   headers={"Prefer": "return=minimal"})
    breaker = CircuitBreaker(day_start, limits)
    breaker.killed = bool(state["killed"])
    decisions = run_cycle(markets, estimator, broker, limits, breaker=breaker, top_n=top_n)
    by_id = {m.market_id: m for m in markets}
    rows = [
        {
            "market_id": d.opportunity.market_id,
            "question": by_id[d.opportunity.market_id].question[:300],
            "side": d.opportunity.side.value,
            "price": d.opportunity.price,
            "prob": d.opportunity.prob,
            "edge": d.opportunity.edge,
            "stake": d.stake,
            "approved": d.approved,
            "reason": d.reason,
        }
        for d in decisions
    ]
    store.save(broker)
    cycle_id = store.log_cycle(len(markets), broker.equity_at_cost, rows)
    halted = breaker.tripped(broker.equity_at_cost)
    return {"cycle_id": cycle_id, "scanned": len(markets), "approved": sum(r["approved"] for r in rows),
            "equity_at_cost": broker.equity_at_cost, "halted": halted, "decisions": rows}
