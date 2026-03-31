# PR-001-DETERMINISTIC-SCORING-CORE-1

## Goal
Harden the explicit scoring formulas and make them reproducible from code + docs.

## Files
- `src/strategy/scoring_v1.py`
- `src/strategy/types.py`
- `docs/SCORING_ALGORITHMS.md`
- `tests/test_scoring_v1.py`

## Exact fixes
- finalize the V1 formulas
- add docstrings and corner-case handling
- keep outputs deterministic
- add score breakdown fields for every term

## Definition of done
- tests pass
- no hidden heuristics
- scoring output is explainable term by term

## Tests
- `pytest -q tests/test_scoring_v1.py`
