# PR-004-DUNE-HISTORICAL-LABELING-1

## Goal
Create the historical truth layer for wallet quality and candidate labeling.

## Files
- `queries/dune/*.sql`
- `scripts/export_dune_labels.py`
- `docs/REPLAY_METRICS.md`

## Exact fixes
- define forward-return labels
- define wallet cohort success rate derivation
- export replay-ready JSONL/CSV

## Definition of done
- one command generates a reproducible label dataset

## Tests
- dry-run query lint + sample export smoke
