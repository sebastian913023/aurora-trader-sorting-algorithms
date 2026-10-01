"""Polymarket taker-fee model: fee = shares * rate * p * (1 - p). Makers pay 0.

Rates are from the research report (page summaries, re-verify against
docs.polymarket.com before any live use).
"""

from __future__ import annotations

CATEGORY_FEE_RATES: dict[str, float] = {
    "crypto": 0.07,
    "sports": 0.05,
    "finance": 0.04,
    "politics": 0.04,
    "tech": 0.04,
    "geopolitics": 0.0,
    "other": 0.05,
}


def fee_rate(category: str) -> float:
    """Fee rate for a category (unknown categories use 'other')."""
    return CATEGORY_FEE_RATES.get(category.lower(), CATEGORY_FEE_RATES["other"])


def taker_fee_per_share(price: float, category: str = "other") -> float:
    """Fee per share, in USD, for buying at ``price``."""
    if not 0.0 < price < 1.0:
        raise ValueError("price must be in (0, 1)")
    return fee_rate(category) * price * (1.0 - price)
