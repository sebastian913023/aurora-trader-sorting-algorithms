"""End-to-end paper cycle: estimate -> edge -> rank -> Kelly -> risk -> fill."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from .estimator import ProbabilityEstimator
from .formulas import fractional_kelly
from .models import Decision, Market, Opportunity
from .paper import PaperBroker
from .ranker import rank_opportunities
from .risk import CircuitBreaker, RiskLimits
from .scanner import evaluate


def size_and_veto(
    opp: Opportunity,
    market: Market,
    broker: PaperBroker,
    bankroll: float,
    limits: RiskLimits,
) -> Decision:
    """Size with fractional Kelly on all-in cost, then apply risk checks."""
    if opp.edge < limits.min_edge:
        return Decision(opp, 0.0, False, "edge below minimum")
    if market.liquidity < limits.min_liquidity:
        return Decision(opp, 0.0, False, "insufficient liquidity")
    if market.days_to_resolution < limits.min_days_to_resolution:
        return Decision(opp, 0.0, False, "too close to resolution")
    cost = opp.price + opp.fee_per_share
    frac = fractional_kelly(opp.prob, cost, limits.kelly_multiplier, limits.max_position_frac)
    stake = frac * bankroll
    room = limits.max_total_exposure_frac * bankroll - broker.exposure
    stake = min(stake, room, broker.cash)
    if stake <= 0:
        return Decision(opp, 0.0, False, "no capacity or no Kelly edge")
    return Decision(opp, stake, True, "approved")


def run_cycle(
    markets: Iterable[Market],
    estimator: ProbabilityEstimator,
    broker: PaperBroker,
    limits: RiskLimits | None = None,
    evidence: Mapping[str, str] | None = None,
    breaker: CircuitBreaker | None = None,
    top_n: int = 10,
) -> list[Decision]:
    """One paper cycle. Best opportunity per market only; returns all decisions."""
    limits = limits or RiskLimits()
    evidence = evidence or {}
    bankroll = broker.equity_at_cost
    if breaker is not None and breaker.tripped(bankroll):
        return []
    by_id: dict[str, Market] = {}
    best: list[Opportunity] = []
    for m in markets:
        by_id[m.market_id] = m
        est = estimator.estimate(m, evidence.get(m.market_id, ""))
        opps = evaluate(m, est.prob)
        best.append(max(opps, key=lambda o: o.edge))
    decisions: list[Decision] = []
    for opp in rank_opportunities(best, limit=top_n):
        d = size_and_veto(opp, by_id[opp.market_id], broker, bankroll, limits)
        if d.approved:
            broker.execute(d)
        decisions.append(d)
    return decisions
