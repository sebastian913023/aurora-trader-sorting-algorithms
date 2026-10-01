"""Tests for the Polymarket paper-trading package (no network)."""

from __future__ import annotations

import math
from types import SimpleNamespace

import pytest

from src.polymarket.estimator import ClaudeEstimator, StubEstimator, parse_estimate
from src.polymarket.fees import taker_fee_per_share
from src.polymarket.formulas import (
    bayes_update, break_even_win_rate, fractional_kelly, kelly_fraction,
    log_return, shrink_to_market,
)
from src.polymarket.models import Market, Opportunity, Side
from src.polymarket.paper import PaperBroker
from src.polymarket.pipeline import run_cycle
from src.polymarket.ranker import rank_opportunities
from src.polymarket.risk import CircuitBreaker, RiskLimits
from src.polymarket.scanner import complement_arb_edge, evaluate
from src.polymarket.stats import brier_score, log_loss, wilson_interval


def mk(mid="m1", bid=0.48, ask=0.50, cat="politics", liq=5000.0) -> Market:
    return Market(mid, "Q?", bid, ask, cat, liq)


def test_fee_formula_peaks_at_half():
    assert taker_fee_per_share(0.5, "crypto") == pytest.approx(0.07 * 0.25)
    assert taker_fee_per_share(0.5, "geopolitics") == 0.0
    assert taker_fee_per_share(0.9) < taker_fee_per_share(0.5)


def test_kelly_binary():
    assert kelly_fraction(0.6, 0.5) == pytest.approx(0.2)
    assert kelly_fraction(0.4, 0.5) == 0.0
    assert fractional_kelly(0.9, 0.5, 0.25, cap=0.05) == 0.05


def test_break_even_equals_cost():
    assert break_even_win_rate(0.62) == 0.62


def test_bayes_update_and_shrink():
    assert bayes_update(0.5, 1.0) == pytest.approx(0.5)
    assert bayes_update(0.5, 3.0) == pytest.approx(0.75)
    assert shrink_to_market(0.9, 0.5, 0.0) == pytest.approx(0.5)
    assert shrink_to_market(0.9, 0.5, 1.0) == pytest.approx(0.9)


def test_log_return():
    assert log_return(100, 110) == pytest.approx(math.log(1.1))
    with pytest.raises(ValueError):
        log_return(0, 1)


def test_stats():
    assert brier_score([1.0, 0.0], [1, 0]) == 0.0
    assert brier_score([0.5, 0.5], [1, 0]) == pytest.approx(0.25)
    assert log_loss([0.5], [1]) == pytest.approx(math.log(2))
    lo, hi = wilson_interval(40, 50)
    assert 0.66 < lo < 0.68 and 0.88 < hi < 0.90


def test_evaluate_edge_net_of_fee():
    opps = {o.side: o for o in evaluate(mk(), 0.60)}
    yes = opps[Side.YES]
    assert yes.edge == pytest.approx(0.60 - 0.50 - 0.04 * 0.25)
    assert opps[Side.NO].edge < 0


def test_complement_arb_none_on_normal_book():
    assert complement_arb_edge(mk()) < 0


def test_ranker_topn_deterministic_ties():
    o = lambda i, e: Opportunity(i, Side.YES, 0.5, 0.6, e, 0.0)
    items = [o("b", 0.1), o("a", 0.1), o("c", 0.2)]
    full = [x.market_id for x in rank_opportunities(items)]
    top = [x.market_id for x in rank_opportunities(items, limit=3)]
    assert full == top == ["c", "a", "b"]


def test_invalid_market_rejected():
    with pytest.raises(ValueError):
        Market("x", "q", 0.6, 0.5)


def test_parse_estimate():
    e = parse_estimate('noise {"probability": 0.7, "confidence": 0.8, "rationale": "r"} x')
    assert e.prob == pytest.approx(0.7) and e.confidence == 0.8
    with pytest.raises(ValueError):
        parse_estimate("nope")
    with pytest.raises(ValueError):
        parse_estimate('{"probability": 1.5}')


class FakeClient:
    def __init__(self, text):
        self.prompts = []
        self.messages = SimpleNamespace(create=self._create)
        self._text = text

    def _create(self, **kw):
        self.prompts.append(kw["messages"][0]["content"])
        return SimpleNamespace(content=[SimpleNamespace(text=self._text)])


def test_claude_estimator_hides_price_and_shrinks():
    client = FakeClient('{"probability": 0.9, "confidence": 1.0, "rationale": "x"}')
    m = mk()
    est = ClaudeEstimator(client=client, max_weight=0.5).estimate(m, "evidence")
    assert "0.5" not in client.prompts[0].split("Evidence")[0].replace("Days", "")
    assert m.mid < est.prob < 0.9


def test_stub_has_zero_edge_no_trades():
    broker = PaperBroker(cash=1000.0)
    ds = run_cycle([mk()], StubEstimator(), broker)
    assert all(not d.approved for d in ds) and broker.positions == []


class Fixed:
    def __init__(self, p):
        self.p = p

    def estimate(self, market, evidence=""):
        from src.polymarket.estimator import Estimate
        return Estimate(self.p, 1.0)


def test_cycle_sizes_caps_and_settles():
    broker = PaperBroker(cash=1000.0)
    ds = run_cycle([mk()], Fixed(0.70), broker)
    d = ds[0]
    assert d.approved and 0 < d.stake <= 0.05 * 1000.0 + 1e-9
    assert broker.cash == pytest.approx(1000.0 - d.stake)
    pnl = broker.settle("m1", yes_won=True)
    assert pnl > 0 and not broker.positions
    # losing path
    broker2 = PaperBroker(cash=1000.0)
    run_cycle([mk()], Fixed(0.70), broker2)
    assert broker2.settle("m1", yes_won=False) < 0


def test_risk_vetoes():
    broker = PaperBroker(cash=1000.0)
    assert not run_cycle([mk(liq=10)], Fixed(0.8), broker)[0].approved
    assert not run_cycle([mk()], Fixed(0.52), broker)[0].approved  # edge < min


def test_total_exposure_cap():
    broker = PaperBroker(cash=1000.0)
    ms = [mk(f"m{i}") for i in range(20)]
    run_cycle(ms, Fixed(0.8), broker, top_n=20)
    assert broker.exposure <= 0.30 * 1000.0 + 1e-6


def test_circuit_breaker():
    broker = PaperBroker(cash=1000.0)
    br = CircuitBreaker(1000.0, RiskLimits())
    br.kill()
    assert run_cycle([mk()], Fixed(0.8), broker, breaker=br) == []
    br2 = CircuitBreaker(1000.0, RiskLimits())
    broker.cash = 900.0
    assert br2.tripped(broker.equity_at_cost)
