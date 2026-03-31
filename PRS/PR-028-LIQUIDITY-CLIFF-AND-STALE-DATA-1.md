# PR-028: LIQUIDITY-CLIFF-AND-STALE-DATA-1

## Goal
Block candidates that look tradable at tiny size but collapse under slightly larger size checks, and increase protection against stale or conflicting source data.

## Files
- `src/ingest/jupiter_route_analyzer.py`
- `src/strategy/execution_gates.py`
- `src/strategy/types.py`
- `tests/test_route_analyzer.py`
- `docs/LIQUIDITY_CLIFF_AND_STALE_DATA.md`

## Exact fixes
- Add size-ladder impact checks (x1, x3, x10) to detect liquidity cliffs.
- Add stronger stale-data penalties for cache-only or old records.
- Add source-conflict detection for major mismatches in security/liquidity context.
- Allow SCALP to be blocked when freshness is too poor for execution-grade confidence.
- Keep route and freshness logic explainable.

## Definition of done
- Liquidity cliffs are represented as a first-class execution risk.
- Stale/conflicting data can suppress or block weak candidates.
- Tests pass.

## Tests
- x10 impact explosion => candidate blocked or heavily penalized
- stale data => SCALP blocked
- conflicting source values => explicit conflict flag or rejection
