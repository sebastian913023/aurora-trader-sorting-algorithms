# Polymarket paper-trading strategies

Paper mode only. No module here sends orders, holds keys, or calls Polymarket.

## Pipeline (`src/polymarket/pipeline.py`)
estimate P(YES) -> net-of-fee edge -> rank (top-N heap) -> fractional Kelly -> risk veto -> simulated fill -> settle.

## Strategy sets
| Set | Where | Notes |
|---|---|---|
| Expected value | `formulas.expected_value_per_share`, `scanner.evaluate` | edge = prob - price - taker fee |
| Kelly | `formulas.kelly_fraction`, `fractional_kelly` | f* = (q-c)/(1-c) on all-in cost c; default quarter Kelly, 5% cap |
| Bayesian updating | `formulas.bayes_update`, `shrink_to_market` | log-odds; model blended toward market by confidence |
| Log returns | `formulas.log_return` | ln(end/start) |
| Complement arb | `scanner.complement_arb_edge` | YES ask + NO ask < 1 net of fees; ignores depth and resolution risk |
| Forecast quality | `stats.py` | Brier, log loss, Wilson CI |

## Claude probability estimates
`ClaudeEstimator` (needs `ANTHROPIC_API_KEY`; model via `AURORA_CLAUDE_MODEL`, default `claude-opus-5-5`) asks for a probability **without showing the market price**, then shrinks toward the market mid (max weight 0.5). `StubEstimator` returns the mid (zero edge) for offline runs. No evidence that an LLM beats liquid Polymarket prices is established: judge it by forward paper Brier/log loss vs the market price, not by win rate.

## Risk defaults (`risk.py`)
min net edge 3c, min liquidity $500, 5% per trade, 30% total exposure, 5% daily-loss circuit breaker, manual kill switch.

## Caveats
- Fee rates in `fees.py` come from research summaries; verify against official docs before live use.
- Break-even win rate = entry price + fee; an 80% win rate is not the goal.
- International Polymarket is close-only for US persons; live trading needs a compliant venue (Polymarket US / Kalshi) and legal review. Not legal or financial advice.
