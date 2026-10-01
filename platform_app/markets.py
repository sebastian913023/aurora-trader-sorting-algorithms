"""Read-only market source (Polymarket Gamma API) with a defensive parser."""

from __future__ import annotations

import json
from typing import Any

import httpx

from src.polymarket.models import Market

GAMMA_URL = "https://gamma-api.polymarket.com/markets"


def _num(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_market(raw: dict[str, Any]) -> Market | None:
    """Convert one Gamma record to a Market, or None if unusable."""
    bid, ask = _num(raw.get("bestBid")), _num(raw.get("bestAsk"))
    if bid is None or ask is None:
        prices = raw.get("outcomePrices")
        if isinstance(prices, str):
            try:
                prices = json.loads(prices)
            except ValueError:
                prices = None
        if not prices:
            return None
        yes = _num(prices[0])
        if yes is None:
            return None
        bid = ask = yes
    if not (0.0 < bid <= ask < 1.0):
        return None
    days = 30.0
    return Market(
        market_id=str(raw.get("id") or raw.get("conditionId") or ""),
        question=str(raw.get("question") or ""),
        yes_bid=bid,
        yes_ask=ask,
        category=str(raw.get("category") or "other").lower(),
        liquidity=_num(raw.get("liquidityNum") or raw.get("liquidity")) or 0.0,
        days_to_resolution=days,
    )


def fetch_markets(limit: int = 50, client: httpx.Client | None = None) -> list[Market]:
    """Fetch active markets; unusable records are skipped."""
    owns = client is None
    client = client or httpx.Client(timeout=15)
    try:
        resp = client.get(
            GAMMA_URL,
            params={"active": "true", "closed": "false", "limit": limit, "order": "liquidityNum", "ascending": "false"},
        )
        resp.raise_for_status()
        data = resp.json()
    finally:
        if owns:
            client.close()
    out = [m for r in data if (m := parse_market(r)) and m.market_id]
    return out
