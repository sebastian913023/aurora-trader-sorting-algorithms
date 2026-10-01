"""Turn markets + probability estimates into net-of-fee opportunities."""

from __future__ import annotations

from .fees import taker_fee_per_share
from .models import Market, Opportunity, Side


def evaluate(market: Market, p_yes: float) -> list[Opportunity]:
    """Both sides of a market, edge net of taker fee (buying at the ask)."""
    out = []
    for side, price, prob in (
        (Side.YES, market.yes_ask, p_yes),
        (Side.NO, market.no_ask, 1.0 - p_yes),
    ):
        if not 0.0 < price < 1.0:
            continue
        fee = taker_fee_per_share(price, market.category)
        out.append(Opportunity(market.market_id, side, price, prob, prob - price - fee, fee))
    return out


def complement_arb_edge(market: Market) -> float:
    """Riskless edge per share pair from buying YES at ask and NO at ask.

    Pays exactly $1 at resolution; edge = 1 - (yes_ask + no_ask) - both fees.
    Positive only if the book is crossed/inefficient. Ignores depth and
    resolution risk (see report)."""
    no_ask = market.no_ask
    fees = taker_fee_per_share(market.yes_ask, market.category) + taker_fee_per_share(no_ask, market.category)
    return 1.0 - (market.yes_ask + no_ask) - fees
