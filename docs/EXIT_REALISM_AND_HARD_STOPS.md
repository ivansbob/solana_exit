# EXIT REALISM AND HARD STOPS

Exit decisions now use **net executable PnL** instead of optimistic gross mark-to-market PnL.

## What changed

- Added exit-time economic fields for execution realism:
  - `PositionState.position_notional_sol`
  - `PositionState.realized_fee_drag_sol`
  - `PositionState.expected_exit_fee_sol`
  - `CandidateSnapshot.estimated_exit_fee_sol`
  - `CandidateSnapshot.dynamic_liquidity_stress`
  - `CandidateSnapshot.smart_money_reference_pnl_pct`
- Added `DynamicExitManager.net_executable_pnl_pct(...)` helper.
- Added an unconditional hard stop (`hard_stop_loss_pct`, default `-12%`).
- Take-profit gates across SCALP/DIP/TREND now key off net executable PnL.
- Dynamic-liquidity routes receive an additional haircut when estimating exits.
- Deeply underwater smart-money reference cohorts apply a bagholder penalty, making exits more defensive.

## Net executable PnL model

`net_executable_pnl_pct` starts from gross unrealized PnL and subtracts:

1. sell impact (`jupiter_sell_impact_bps`),
2. dynamic-liquidity haircut (`route_uses_dynamic_liquidity_share` weighted),
3. total fee drag (`round_trip_fee_sol`, candidate exit fees, and position-level fees).

If smart-money reference holders are deeply underwater (default threshold `<= -25%`),
a penalty is applied to suppress over-optimistic profit exits.

## Configurability

All thresholds live in `ExitThresholds` and can be tuned without changing core logic.

## Safety objective

A paper-trade exit is considered valid only if it remains plausible after realistic impact and fee drag.
