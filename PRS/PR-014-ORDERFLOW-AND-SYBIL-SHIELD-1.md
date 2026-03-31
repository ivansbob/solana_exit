# PR-014-ORDERFLOW-AND-SYBIL-SHIELD-1

## Goal
Upgrade the bootstrap from coarse buy/sell counts to execution-aware orderflow and add hard protection against sybil-like clusters and fake one-way liquidity.

## Files
- `src/strategy/types.py`
- `src/strategy/execution_gates.py`
- `src/strategy/scoring_v2.py`
- `data_contracts/candidate_snapshot.schema.json`
- `tests/test_strategy_upgrade_v2.py`
- `docs/SCORING_ALGORITHMS.md`

## Exact fixes
- Use `taker_buy_volume_usd` / `taker_sell_volume_usd` in scoring instead of raw counts for the preferred path.
- Add `jupiter_sell_impact_bps` and reject strong buy/sell asymmetry.
- Add `sybil_cluster_share_pct` and block highly clustered launches.
- Add `volume_authenticity_ratio` and turn it into a multiplicative kill-switch.

## Definition of done
- Scoring prefers taker-dollar imbalance in `scoring_v2.py`.
- Gates reject toxic sell asymmetry and sybil-heavy candidates.
- Tests cover pass and fail cases.

## Tests
- asymmetry gate rejection
- sybil gate rejection
- authenticity kill-switch zeroing score
