# PR-024: SOLANA-NETWORK-REALISM-1

## Goal
Improve paper-trade realism for tiny-capital Solana execution by modeling token-account rent drag, rent reclaim, and the cost of failed transaction attempts.

## Files
- `src/paper/mev_simulator.py`
- `src/strategy/types.py`
- `tests/test_mev_simulator.py`
- `docs/SOLANA_NETWORK_REALISM.md`

## Exact fixes
- Add ATA rent fee fields and simulation assumptions.
- Charge token-account rent on first entry when no ATA exists yet.
- Support optional rent reclaim on full exit / account close assumptions.
- Model failed transaction fee drag instead of treating failed attempts as free.
- Break out network cost components clearly in simulator outputs when possible.

## Definition of done
- Tiny-capital replay becomes more pessimistic and realistic.
- Failed attempts have real cost.
- ATA economics are represented explicitly.
- Tests pass.

## Tests
- first entry with no ATA charges ATA drag
- full exit may reclaim ATA rent if configured
- failed fills are not free
- simulator reflects cost breakdowns
