"""Trading order book for Aurora Trader."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Order:
    """A buy or sell order in the market."""

    trader: str
    side: str
    price: float
    quantity: float


class OrderBook:
    """A simple order book that sorts bids and asks by best price."""

    def __init__(self) -> None:
        self.bids: List[Order] = []
        self.asks: List[Order] = []

    def add_order(self, order: Order) -> None:
        """Add a new order to the order book."""
        if order.side.lower() == "buy":
            self.bids.append(order)
        elif order.side.lower() == "sell":
            self.asks.append(order)
        else:
            raise ValueError("side must be 'buy' or 'sell'")

    def best_bid(self) -> Order | None:
        """Return the highest-priced buy order."""
        if not self.bids:
            return None
        return sorted(self.bids, key=lambda order: order.price, reverse=True)[0]

    def best_ask(self) -> Order | None:
        """Return the lowest-priced sell order."""
        if not self.asks:
            return None
        return sorted(self.asks, key=lambda order: order.price)[0]

    def sorted_bids(self) -> List[Order]:
        """Return all bids sorted by descending price."""
        return sorted(self.bids, key=lambda order: order.price, reverse=True)

    def sorted_asks(self) -> List[Order]:
        """Return all asks sorted by ascending price."""
        return sorted(self.asks, key=lambda order: order.price)

    def match_orders(self) -> List[tuple[Order, Order]]:
        """A simplified matching process: pair buy orders and sell orders.

        This is intentionally simple and educational, not a production matching
        engine.
        """
        matches: List[tuple[Order, Order]] = []
        bids = self.sorted_bids()
        asks = self.sorted_asks()

        for buy in bids:
            for sell in asks:
                if buy.price >= sell.price:
                    matches.append((buy, sell))
                    break

        return matches
