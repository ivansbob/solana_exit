# PR-003-REGIME-ROUTER-SCALP-TREND-1

## Goal
Classify candidates into SCALP, TREND, or IGNORE before scoring.

## Files
- `src/strategy/regime_classifier.py`
- `docs/METRIC_CATALOG.md`
- tests

## Exact fixes
- implement deterministic routing
- expose confidence and reason
- wire scorer to regime classifier

## Definition of done
- same candidate always gets same regime
- clear reasons for IGNORE

## Tests
- add unit tests for all three routes
