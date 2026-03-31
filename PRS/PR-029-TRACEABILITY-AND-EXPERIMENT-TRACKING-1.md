# PR-029: TRACEABILITY-AND-EXPERIMENT-TRACKING-1

## Goal
Improve debugging, ablation, and parameter iteration by making decisions traceable and experiment outputs reproducible.

## Files
- `src/reports/decision_trace.py`
- `src/reports/experiment_log.py`
- `docs/TRACEABILITY_AND_EXPERIMENTS.md`
- `tests/`

## Exact fixes
- Record gate outcomes, regime outcomes, scorer multipliers, and exit reasons in a structured trace.
- Persist threshold/weight settings for replay runs.
- Add simple experiment ledger support for replay comparisons.
- Make it easy to explain why a candidate was blocked, accepted, or exited.

## Definition of done
- Decisions become reconstructable after the fact.
- Replay runs can be compared across parameter sets.
- Minimal tests and docs exist.

## Tests
- decision trace contains gate + regime + scorer context
- experiment log persists run metadata deterministically
