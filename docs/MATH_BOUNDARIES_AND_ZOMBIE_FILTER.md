# MATH BOUNDARIES AND ZOMBIE FILTER

## Implemented in PR-023

This upgrade addresses two boundary failures in deterministic scoring:
- over-reactive micro-volume z-scores on tiny/low-liquidity pools
- false-positive breakout/trend signals on old inactive ("zombie") pools

### 1) Liquidity-aware dynamic denominator floor (micro-volume z-score)

`OpportunityScorerV2._micro_vol_accel_z()` now uses:
- observed micro std (`std_volume_5m_per_min_usd`) when reliable
- **or** a dynamic floor based on baseline volume and pool liquidity

Formula:
- `liquidity_penalty = max(1.0, micro_z_liquidity_reference_usd / liquidity_usd)`
- `baseline_floor = baseline_1m * micro_z_baseline_floor_ratio * liquidity_penalty`
- `denominator = max(observed_std, micro_z_min_std_floor_usd_per_min, baseline_floor)`

Result:
- low-liquidity + low-variance pools can no longer saturate z-score from tiny absolute spikes
- deeper pools remain responsive because penalty relaxes as liquidity grows

All parameters remain configurable through `OpportunityScorerV2(...)`.

### 2) Zombie-token filter

`RegimeClassifier` and `TinyCapitalRiskGates` now reject candidates when:
- `pair_age_seconds >= zombie_min_pool_age_seconds`
- and baseline per-minute activity is effectively dead:
  `mean_volume_5m_per_min_usd` (fallback `mean_volume_1h_usd/60`) `<= zombie_max_baseline_volume_1m_usd`

This explicitly blocks old inactive tokens that briefly spike.

Thresholds are configurable in both components.

### 3) Clarified concentration semantics: EOA vs LP/PDA/system

Concentration controls now use `eoa_wallet_concentration` (externally owned addresses only).

Fallback behavior:
- if `eoa_wallet_concentration` is unavailable (`0`), legacy `top_wallet_concentration` is used

This avoids penalizing LP vault / PDA / system-account-heavy distributions as if they were whale-held EOAs, while preserving backward compatibility.
