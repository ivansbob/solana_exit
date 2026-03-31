# PR-022: EXIT-REALISM-AND-HARD-STOPS-1

## Goal
Make exit decisions depend on net executable PnL rather than naive gross PnL, and add unconditional hard-stop protection for tiny-capital Solana paper trading.

## Files
- `src/strategy/exit_manager.py`
- `src/strategy/types.py`
- `tests/test_exit_manager.py`
- `docs/EXIT_REALISM_AND_HARD_STOPS.md`

## Exact fixes
- Add missing exit-time fields needed for executable-PnL logic.
- Introduce a helper that computes net executable PnL after sell impact and fee drag.
- Add unconditional hard stop-loss for severe downside.
- Make take-profit decisions use net executable PnL, not gross mark-to-market PnL.
- Add more defensive behavior when smart-money reference holders are deeply underwater.
- Preserve regime-aware behavior across SCALP, DIP, and TREND.

## Definition of done
- Exit logic is based on executable economics.
- Hard stop-loss exists and is covered by tests.
- Existing time-stop and decay logic still work.
- Tests pass.

## Tests
- gross green but net flat/negative => no optimistic profit exit
- hard stop-loss triggers immediately
- dynamic-liquidity haircut reduces executable PnL
- bagholder penalty makes exits more defensive
- regime-aware time-stop behavior still works
