"""Probability estimation seam. Claude API implementation + offline stub."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Protocol

from .formulas import clamp_prob, shrink_to_market
from .models import Market

DEFAULT_MODEL = os.environ.get("AURORA_CLAUDE_MODEL", "claude-opus-5-5")


@dataclass(frozen=True)
class Estimate:
    prob: float  # P(YES)
    confidence: float  # 0..1, used as shrinkage weight
    rationale: str = ""


class ProbabilityEstimator(Protocol):
    def estimate(self, market: Market, evidence: str = "") -> Estimate: ...


class StubEstimator:
    """Returns the market mid: zero edge by construction. Offline default."""

    def estimate(self, market: Market, evidence: str = "") -> Estimate:
        return Estimate(prob=market.mid, confidence=0.0, rationale="stub: market mid")


_PROMPT = (
    "You are a calibrated forecaster. Estimate the probability that the market "
    "question resolves YES. Do not anchor on any price; base it on the evidence "
    "and base rates. Reply with ONLY JSON: "
    '{{"probability": <0-1>, "confidence": <0-1>, "rationale": "<one sentence>"}}.\n\n'
    "Question: {question}\nDays to resolution: {days}\nEvidence:\n{evidence}\n"
)


def parse_estimate(text: str) -> Estimate:
    """Parse the model's JSON reply; raises ValueError if unusable."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("no JSON object in reply")
    data = json.loads(match.group(0))
    prob = float(data["probability"])
    conf = float(data.get("confidence", 0.5))
    if not (0.0 <= prob <= 1.0 and 0.0 <= conf <= 1.0):
        raise ValueError("probability/confidence out of range")
    return Estimate(clamp_prob(prob), conf, str(data.get("rationale", ""))[:300])


class ClaudeEstimator:
    """Estimates P(YES) with the Claude API, blended toward the market price.

    The market price is deliberately NOT shown to the model (anchoring); it is
    only used afterwards for log-odds shrinkage, capped by ``max_weight``.
    Pass ``client`` (anything with ``messages.create``) to avoid network in tests.
    """

    def __init__(self, client: Any = None, model: str = DEFAULT_MODEL, max_weight: float = 0.5) -> None:
        if client is None:
            import anthropic  # lazy: reads ANTHROPIC_API_KEY

            client = anthropic.Anthropic()
        self._client = client
        self._model = model
        self._max_weight = max_weight

    def estimate(self, market: Market, evidence: str = "") -> Estimate:
        reply = self._client.messages.create(
            model=self._model,
            max_tokens=300,
            messages=[{"role": "user", "content": _PROMPT.format(
                question=market.question, days=market.days_to_resolution,
                evidence=evidence or "(none)")}],
        )
        text = "".join(getattr(b, "text", "") for b in reply.content)
        raw = parse_estimate(text)
        weight = min(self._max_weight, raw.confidence * self._max_weight)
        blended = shrink_to_market(raw.prob, market.mid, weight)
        return Estimate(blended, raw.confidence, raw.rationale)
