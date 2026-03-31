# Dollar-Aware Exits and Failed-TX Drag

This follow-up task shifts tiny-capital realism from gross percentage PnL toward executable economics.

Key idea:
- a visually green trade can still be net-negative after sell impact, failed-attempt fee drag, Jito/priority burden, and other route friction.

Repository intent:
- keep replay and paper assumptions pessimistic
- prefer executable net value over cosmetic mark-to-market PnL

## What was implemented

- `DynamicExitManager` now exposes:
  - `gross_mark_to_market_pnl_pct(...)` for cosmetic mark-to-market view.
  - `net_executable_pnl_pct(...)` for executable net percent after impact/liquidity/fees.
  - `net_executable_pnl_sol(...)` for absolute SOL economics on tiny notional.
- Exit decisions continue to use executable net PnL for take-profit/time-stop logic.

- `BootstrapMEVSimulator` now models failed-attempt drag explicitly:
  - configurable thresholds via `SimulationThresholds` (deterministic constants only),
  - `failed_attempt_fee_drag_sol` is charged as expected failed probability × per-attempt fee,
  - total `fee_drag_sol` now includes both base cost and failed-attempt drag.

## Determinism and configurability

- No stochastic behavior was added.
- All realism knobs are configurable through dataclass thresholds.
- No paid dependency or external service is required.
