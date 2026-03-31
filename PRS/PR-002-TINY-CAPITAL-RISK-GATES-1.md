# PR-002-TINY-CAPITAL-RISK-GATES-1

## Goal
Implement strict no-trade gates for tiny-size execution realism.

## Files
- `src/strategy/execution_gates.py`
- `docs/SCORING_ALGORITHMS.md`
- `tests/test_scoring_v1.py`

## Exact fixes
- separate soft score from hard skip rules
- add reasons for each rejection
- expose gate decisions in a machine-readable form

## Definition of done
- every rejected trade has an explicit reason
- gate order is deterministic

## Tests
- add tests for liquidity, impact, fee, concentration, freshness rejections
