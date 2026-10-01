"""FastAPI entrypoint for Vercel (zero-config). Paper trading only."""

from __future__ import annotations

import hmac
import os

from fastapi import Depends, FastAPI, Header, HTTPException

from platform_app.cycle import run_persisted_cycle
from platform_app.markets import fetch_markets
from platform_app.store import Store
from src.polymarket.estimator import ClaudeEstimator

app = FastAPI(title="Alpha Engine", version="1.0.0", docs_url=None, redoc_url=None)


def require_secret(authorization: str | None = Header(default=None)) -> None:
    """Fail closed: mutating routes need Bearer CRON_SECRET (Vercel Cron sends it)."""
    secret = os.environ.get("CRON_SECRET", "")
    expected = f"Bearer {secret}"
    if not secret or not authorization or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="unauthorized")


def get_store() -> Store:
    try:
        return Store()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/health")
def health() -> dict[str, object]:
    return {
        "ok": True,
        "mode": "paper",
        "estimator_configured": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "store_configured": bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_ROLE_KEY")),
    }


@app.get("/api/state")
def state(store: Store = Depends(get_store)) -> dict[str, object]:
    broker, s = store.load()
    return {
        "mode": "paper", "cash": broker.cash, "exposure": broker.exposure, "equity_at_cost": broker.equity_at_cost,
        "realized_pnl": broker.realized_pnl, "open_positions": len(broker.positions), "killed": s["killed"],
        **store.recent(),
    }


@app.api_route("/api/cron/cycle", methods=["GET", "POST"], dependencies=[Depends(require_secret)])
def cycle(store: Store = Depends(get_store)) -> dict[str, object]:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(status_code=503, detail="ANTHROPIC_API_KEY not set")
    markets = fetch_markets(limit=int(os.environ.get("AE_SCAN_LIMIT", "40")))
    return run_persisted_cycle(store, markets, ClaudeEstimator(), top_n=int(os.environ.get("AE_TOP_N", "5")))


@app.post("/api/kill", dependencies=[Depends(require_secret)])
def kill(store: Store = Depends(get_store)) -> dict[str, bool]:
    store._req("PATCH", "ae_state?id=eq.1", json={"killed": True}, headers={"Prefer": "return=minimal"})
    return {"killed": True}
