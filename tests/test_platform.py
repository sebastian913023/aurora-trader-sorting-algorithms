"""Tests for the web platform glue (fake Supabase; no network)."""

from __future__ import annotations

import httpx
import pytest
from fastapi.testclient import TestClient

from api.index import app, get_store
from platform_app.cycle import run_persisted_cycle
from platform_app.markets import parse_market
from platform_app.store import Store
from src.polymarket.estimator import Estimate
from src.polymarket.models import Market


class FakeSupabase:
    """Minimal PostgREST stand-in backed by dicts."""

    def __init__(self) -> None:
        self.state: dict | None = None
        self.cycles: list[dict] = []
        self.decisions: list[dict] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        import json

        path = request.url.path.split("/rest/v1/")[1]
        body = json.loads(request.content) if request.content else None
        if path.startswith("ae_state"):
            if request.method == "GET":
                return httpx.Response(200, json=[self.state] if self.state else [])
            if request.method == "POST":
                self.state = {"realized_pnl": 0.0, "positions": [], "killed": False, **body}
            else:
                self.state.update(body)
            return httpx.Response(204)
        if path.startswith("ae_cycles"):
            if request.method == "POST":
                self.cycles.append({"id": len(self.cycles) + 1, **body})
                return httpx.Response(201, json=[self.cycles[-1]])
            return httpx.Response(200, json=self.cycles)
        if request.method == "POST":
            self.decisions.extend(body)
            return httpx.Response(204)
        return httpx.Response(200, json=self.decisions)


class FixedEstimator:
    def __init__(self, p: float) -> None:
        self.p = p

    def estimate(self, market: Market, evidence: str = "") -> Estimate:
        return Estimate(prob=self.p, confidence=0.9, rationale="fixed")


def make_store(fake: FakeSupabase) -> Store:
    client = httpx.Client(transport=httpx.MockTransport(fake.handler))
    return Store("https://x.supabase.co", "svc", client)


MARKET = Market("m1", "Will X happen?", 0.40, 0.42, "other", liquidity=5000.0)


def test_parse_market_handles_string_prices_and_rejects_junk() -> None:
    m = parse_market({"id": 7, "question": "Q", "outcomePrices": '["0.31","0.69"]', "liquidityNum": 900})
    assert m is not None and m.yes_ask == pytest.approx(0.31) and m.liquidity == 900
    assert parse_market({"id": 1, "outcomePrices": '["1.0","0.0"]'}) is None
    assert parse_market({"id": 2}) is None


def test_cycle_persists_state_and_decisions() -> None:
    fake = FakeSupabase()
    out = run_persisted_cycle(make_store(fake), [MARKET], FixedEstimator(0.80))
    assert out["approved"] == 1
    assert fake.state["cash"] < 10000.0 and len(fake.state["positions"]) == 1
    assert len(fake.cycles) == 1 and fake.decisions[0]["approved"] is True


def test_kill_switch_halts_trading() -> None:
    fake = FakeSupabase()
    store = make_store(fake)
    store.load()
    fake.state["killed"] = True
    out = run_persisted_cycle(store, [MARKET], FixedEstimator(0.80))
    assert out["approved"] == 0 and out["halted"] is True and fake.state["cash"] == 10000.0


def test_cron_route_fails_closed_without_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CRON_SECRET", raising=False)
    client = TestClient(app)
    assert client.get("/api/cron/cycle").status_code == 401
    monkeypatch.setenv("CRON_SECRET", "s3cret")
    assert client.get("/api/cron/cycle", headers={"Authorization": "Bearer wrong"}).status_code == 401


def test_cycle_requires_estimator_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CRON_SECRET", "s3cret")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    app.dependency_overrides[get_store] = lambda: make_store(FakeSupabase())
    try:
        r = TestClient(app).get("/api/cron/cycle", headers={"Authorization": "Bearer s3cret"})
        assert r.status_code == 503
    finally:
        app.dependency_overrides.clear()


def test_health_and_state(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = FakeSupabase()
    app.dependency_overrides[get_store] = lambda: make_store(fake)
    try:
        c = TestClient(app)
        assert c.get("/api/health").json()["mode"] == "paper"
        s = c.get("/api/state").json()
        assert s["cash"] == 10000.0 and s["open_positions"] == 0
    finally:
        app.dependency_overrides.clear()
