# PR-016-SMART-MONEY-DISTANCE-AND-BUNDLE-SHIELD-1

## Goal
Reduce the risk of becoming exit liquidity for early smart-money cohorts and block highly cornered launches.

## Files
- `src/strategy/types.py`
- `src/strategy/scoring_v2.py`
- `src/strategy/execution_gates.py`
- `queries/dune/block_0_snipe_pct.sql`
- `docs/METRIC_CATALOG.md`

## Exact fixes
- Add `distance_from_smart_entry_pct` and reduce or block signals that are too extended from smart-money entry.
- Add `block_0_snipe_pct` as a hard launch-quality metric.
- Document how to label both metrics from historical data.

## Definition of done
- Too-extended smart-money distance is penalized in scoring.
- Excessive block-0 sniping is blocked.
- Query scaffold exists for historical labeling.
