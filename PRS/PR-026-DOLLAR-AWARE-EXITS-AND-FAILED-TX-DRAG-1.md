# PR-026: DOLLAR-AWARE-EXITS-AND-FAILED-TX-DRAG-1

## Goal
Move exit and replay realism from gross percentage logic to executable tiny-capital economics in absolute terms, including failed-transaction fee drag.

## Files
- `src/strategy/exit_manager.py`
- `src/paper/mev_simulator.py`
- `src/strategy/types.py`
- `tests/test_exit_manager.py`
- `tests/test_mev_simulator.py`
- `docs/DOLLAR_AWARE_EXITS_AND_FAILED_TX_DRAG.md`

## Exact fixes
- Add executable dollar/SOL-aware PnL helpers.
- Distinguish gross mark-to-market PnL from executable net PnL.
- Charge failed entry attempts with realistic fee drag instead of treating them as free misses.
- Make exit logic prefer net executable value, not cosmetic percentage gains.
- Preserve pessimistic replay assumptions for tiny-capital trading.

## Definition of done
- Exit logic can evaluate net executable PnL in absolute economics.
- Failed transaction attempts reduce simulated performance.
- Existing exit behavior remains backward-compatible where possible.
- Tests pass.

## Tests
- gross positive but net executable negative => no optimistic take-profit
- failed fills produce fee drag
- net executable PnL is lower than gross when sell impact is high
- replay cost breakdown includes failed attempt drag
