"""Supabase (PostgREST) persistence over httpx. Service-role key stays server-side."""

from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any

import httpx

from src.polymarket.models import Side
from src.polymarket.paper import PaperBroker, Position

START_CASH = float(os.environ.get("AE_START_CASH", "10000"))


class Store:
    def __init__(self, url: str | None = None, key: str | None = None, client: httpx.Client | None = None) -> None:
        self.url = (url or os.environ.get("SUPABASE_URL", "")).rstrip("/")
        self.key = key or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
        if not self.url or not self.key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required")
        self.http = client or httpx.Client(timeout=15)
        self.h = {"apikey": self.key, "Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}

    def _req(self, method: str, path: str, **kw: Any) -> Any:
        r = self.http.request(method, f"{self.url}/rest/v1/{path}", headers={**self.h, **kw.pop("headers", {})}, **kw)
        r.raise_for_status()
        return r.json() if r.content else None

    def load(self) -> tuple[PaperBroker, dict[str, Any]]:
        rows = self._req("GET", "ae_state?id=eq.1&select=*")
        if not rows:
            row = {"id": 1, "cash": START_CASH, "day_start_equity": START_CASH}
            self._req("POST", "ae_state", json=row, headers={"Prefer": "return=minimal"})
            rows = [{**row, "realized_pnl": 0.0, "positions": [], "killed": False}]
        s = rows[0]
        broker = PaperBroker(
            cash=s["cash"],
            positions=[Position(p["market_id"], Side(p["side"]), p["shares"], p["cost"]) for p in s["positions"]],
            realized_pnl=s["realized_pnl"],
        )
        return broker, s

    def save(self, broker: PaperBroker) -> None:
        body = {
            "cash": broker.cash,
            "realized_pnl": broker.realized_pnl,
            "positions": [{**asdict(p), "side": p.side.value} for p in broker.positions],
        }
        self._req("PATCH", "ae_state?id=eq.1", json=body, headers={"Prefer": "return=minimal"})

    def log_cycle(self, scanned: int, equity: float, decisions: list[dict[str, Any]]) -> int:
        cyc = self._req(
            "POST", "ae_cycles", json={"scanned": scanned, "approved": sum(d["approved"] for d in decisions), "equity": equity},
            headers={"Prefer": "return=representation"},
        )[0]
        if decisions:
            self._req("POST", "ae_decisions", json=[{**d, "cycle_id": cyc["id"]} for d in decisions], headers={"Prefer": "return=minimal"})
        return int(cyc["id"])

    def recent(self, limit: int = 50) -> dict[str, Any]:
        return {
            "cycles": self._req("GET", f"ae_cycles?select=*&order=id.desc&limit={limit}"),
            "decisions": self._req("GET", f"ae_decisions?select=*&order=id.desc&limit={limit}"),
        }
