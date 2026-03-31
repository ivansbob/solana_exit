# PR-019: HYPER-REALISM-SIMULATOR-1

## Goal
Make paper-trade replay materially harder by introducing adverse selection, local fee contention, and cache-drift realism.

## Files
- `src/paper/mev_simulator.py`
- `src/strategy/types.py`
- `src/strategy/execution_gates.py`
- `tests/test_mev_simulator.py`
- `docs/ABYSSAL_ZONE_UPGRADES.md`

## Exact fixes
- Add `local_pool_p75_priority_fee_lamports`, `jito_tip_hurdle_sol`, and `amm_reserve_drift_ratio` to the contract.
- Make fill failure probability increase when the next bar strongly rips upward.
- Add extra slippage and failure probability when aggregator-vs-pool drift is large.
- Distinguish generic priority fees from pool-specific fee wars.

## Definition of done
- Simulator exposes deterministic inputs and outputs.
- Execution gates can reject locally expensive pools.
- Replay can model failure bias against the trader when the market runs away.

## Tests
- high next_return_pct => worse fill probability
- high local pool fee => higher failure probability or gate rejection
- large amm_reserve_drift_ratio => cache-lag risk status
