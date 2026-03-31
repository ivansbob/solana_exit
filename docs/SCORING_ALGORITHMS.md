# SCORING_ALGORITHMS

## Why v2 exists
The bootstrap keeps `scoring_v1.py` as a simple baseline, but the preferred model is now `scoring_v2.py`.

The upgrades address four common failure modes in tiny-capital Solana paper trading:
- 1-hour baseline trap on very young tokens
- buy-only impact blindness
- linear scoring that can be overwhelmed by fake momentum
- no explicit dip regime / no explicit exit realism

## v2 scoring principles
1. Prefer **microstructure** over coarse 1h baselines
2. Prefer **taker orderflow** over raw trade counts
3. Apply **quality multipliers / kill-switches** for fake volume and sybil clusters
4. Score `SCALP`, `TREND`, and `DIP` separately
5. Use **round-trip execution costs**, not just entry costs

## Key formulas

### Micro volume acceleration
`micro_vol_accel_z = (volume_1m_usd - mean_volume_5m_per_min_usd) / std_volume_5m_per_min_usd`

### Taker imbalance
Use taker buy / taker sell dollar flow instead of raw buy/sell counts.

### Quality multiplier
The score is multiplied down or to zero when:
- `volume_authenticity_ratio < 0.40`
- `sybil_cluster_share_pct > 25`
- `block_0_snipe_pct > 15`
- `distance_from_smart_entry_pct` is too high

### DIP recovery score
Favors healthy pullbacks (`15%..40%`) where smart wallets show positive netflow during the dip.

## Threshold defaults
- `SCALP`: 1.30
- `TREND`: 1.40
- `DIP`: 1.35

These are **starting defaults**, not truth. They should be recalibrated by replay and ablation.
