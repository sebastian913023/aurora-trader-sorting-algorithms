"""Expected value, Kelly, Bayesian updating, log returns."""

from __future__ import annotations

import math

_EPS = 1e-9


def clamp_prob(p: float) -> float:
    return min(max(p, _EPS), 1.0 - _EPS)


def logit(p: float) -> float:
    p = clamp_prob(p)
    return math.log(p / (1.0 - p))


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def expected_value_per_share(prob: float, cost: float) -> float:
    """EV of paying ``cost`` for a share paying $1 with probability ``prob``."""
    return prob - cost


def break_even_win_rate(cost: float) -> float:
    """Win rate needed to break even equals the all-in cost per share."""
    return cost


def kelly_fraction(prob: float, cost: float) -> float:
    """Full Kelly for a binary contract: f* = (q - c) / (1 - c); 0 if no edge."""
    if not 0.0 < cost < 1.0:
        raise ValueError("cost must be in (0, 1)")
    return max(0.0, (prob - cost) / (1.0 - cost))


def fractional_kelly(prob: float, cost: float, multiplier: float = 0.25, cap: float = 0.05) -> float:
    """Kelly scaled by ``multiplier`` (default quarter Kelly), capped at ``cap``."""
    return min(cap, multiplier * kelly_fraction(prob, cost))


def bayes_update(prior: float, likelihood_ratio: float) -> float:
    """Posterior from prior probability and a likelihood ratio (log-odds form)."""
    if likelihood_ratio <= 0:
        raise ValueError("likelihood_ratio must be > 0")
    return sigmoid(logit(prior) + math.log(likelihood_ratio))


def shrink_to_market(model_prob: float, market_prob: float, weight: float) -> float:
    """Blend in log-odds: weight=0 trusts the market, weight=1 trusts the model."""
    if not 0.0 <= weight <= 1.0:
        raise ValueError("weight must be in [0, 1]")
    return sigmoid(weight * logit(model_prob) + (1.0 - weight) * logit(market_prob))


def log_return(start: float, end: float) -> float:
    """Continuously-compounded return ln(end/start)."""
    if start <= 0 or end <= 0:
        raise ValueError("values must be positive")
    return math.log(end / start)
