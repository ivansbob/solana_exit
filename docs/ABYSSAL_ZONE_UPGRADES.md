# Abyssal Zone Upgrades

This document captures the next realism layer after the v3 bootstrap.

## New metrics added to the bootstrap contract

- `organic_taker_volume_ratio`
- `signed_buy_ratio`
- `transfer_hook_present`
- `local_pool_p75_priority_fee_lamports`
- `jito_tip_hurdle_sol`
- `amm_reserve_drift_ratio`
- `base_amm_liquidity_share`
- `route_uses_dynamic_liquidity_share`

## Why these metrics exist

### 1. Signed-buy verification
We do not treat passive inbound token transfers as proof of conviction. Smart-money
signals are only trusted when the wallet appears to have signed a paid buy or a
swap-like transaction.

### 2. Transfer Hook hard block
Token-2022 `TransferHook` is treated as a hard no-trade condition in the bootstrap.
That is conservative by design: the project is optimizing for survivability on tiny
capital rather than coverage.

### 3. Local fee contention
Global priority fees can understate the fee war around a single hot pool. We therefore
reserve a separate field for local pool contention and gate on it independently.

### 4. Jito hurdle realism
Tiny-capital replay should not assume that every interesting move is tradable through
cheap public routing. The bootstrap now carries a separate `jito_tip_hurdle_sol` field
so replay and scoring can punish setups whose expected move is too small to overcome
entry + exit landing costs.

### 5. AMM reserve drift / aggregator cache lag
When direct pool reserves drift meaningfully away from the aggregator quote, replay
should not assume a clean marketable fill. The bootstrap now treats large drift as a
hard execution warning and optionally as a fill failure condition.

## Bootstrap behavior

The current repo intentionally stops short of claiming these heuristics are universally
correct. They are defaults for replay calibration.

## Recommended implementation order

1. PR-018 ORDERFLOW-PURITY-AND-GHOST-BIDS-1
2. PR-019 HYPER-REALISM-SIMULATOR-1
3. PR-020 ANTI-SPOOFING-AND-HOOK-SHIELD-1
4. PR-021 MICRO-CAPITAL-JITO-REALISM-1
