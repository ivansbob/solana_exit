# PR-017-LIQUIDITY-QUALITY-AND-SLIPPAGE-REALISM-1

## Goal
Improve tiny-capital realism by modeling the round trip, not just the entry, and by making replay less optimistic during volatile moments.

## Files
- `src/strategy/types.py`
- `src/strategy/execution_gates.py`
- `src/strategy/scoring_v2.py`
- `src/paper/mev_simulator.py`
- `docs/EXECUTION_AND_EXIT_UPGRADES.md`

## Exact fixes
- Keep `round_trip_fee_sol` in the contract and use it in gates/scoring.
- Model failed fills / degraded fills under high momentum.
- Penalize replay when the expected fill environment is hostile to tiny size.

## Definition of done
- Replay can simulate degraded fills.
- The bootstrap no longer treats every high-momentum candidate as fully fillable.
