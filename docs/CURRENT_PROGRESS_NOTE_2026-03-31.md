# Current Progress Note — 2026-03-31

The bootstrap is now beyond the original v1/v2 research shell.

## What is already in the repo

- tiny-capital hard gates
- SCALP / TREND / DIP regime routing
- deterministic scoring core
- dynamic exit manager
- MEV realism placeholder
- anti-rug, anti-sybil, anti-block0 filters
- basic smart-money distance awareness

## What was just added in this upgrade

- signer-only smart-money verification field (`signed_buy_ratio`)
- Token-2022 Transfer Hook hard gate field (`transfer_hook_present`)
- local pool fee contention field (`local_pool_p75_priority_fee_lamports`)
- Jito hurdle realism field (`jito_tip_hurdle_sol`)
- AMM reserve drift / aggregator cache-lag field (`amm_reserve_drift_ratio`)
- Jupiter route quality analyzer scaffold (`base_amm_liquidity_share`, dynamic-liquidity share)
- new PR tasks 018–021 with Codex prompts

## Intent

This remains a research-first, replay-first, paper-trade-first repository. The goal is not to promise profitability. The goal is to make backtests and paper results harder to fake.

## Added follow-up bootstrap tasks

The repository now also includes planned follow-up tasks for:
- PR-022-EXIT-REALISM-AND-HARD-STOPS-1
- PR-023-MATH-BOUNDARIES-AND-ZOMBIE-FILTER-1
- PR-024-SOLANA-NETWORK-REALISM-1
- PR-025-MICROSTRUCTURE-AND-OVERHANG-SHIELD-1

These were added as repository-native PR tasks plus Codex prompts so future continuation can start from the repo itself without reconstructing context from chat.


## Additional continuation tasks added in this update

The repository now also includes the next continuation layer:
- PR-026-DOLLAR-AWARE-EXITS-AND-FAILED-TX-DRAG-1
- PR-027-FUNDING-ENTROPY-AND-MEV-VOLUME-STRIP-1
- PR-028-LIQUIDITY-CLIFF-AND-STALE-DATA-1
- PR-029-TRACEABILITY-AND-EXPERIMENT-TRACKING-1

## Recommended next starting point

The recommended next executable Codex task is:
- `PR-022-EXIT-REALISM-AND-HARD-STOPS-1`

This is documented in `docs/START_NEXT_WITH_CODEX.md`.
