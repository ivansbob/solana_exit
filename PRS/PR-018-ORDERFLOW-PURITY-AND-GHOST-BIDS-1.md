# PR-018: ORDERFLOW-PURITY-AND-GHOST-BIDS-1

## Goal
Differentiate organic directional orderflow from MEV/arbitrage noise and add route-quality awareness so the bootstrap stops overrating dynamic-liquidity mirages.

## Files
- `src/strategy/types.py`
- `src/strategy/scoring_v2.py`
- `src/ingest/jupiter_route_analyzer.py`
- `tests/test_route_analyzer.py`
- `docs/ABYSSAL_ZONE_UPGRADES.md`

## Exact fixes
- Introduce `organic_taker_volume_ratio` into the candidate contract.
- Add a multiplicative kill-switch when organic orderflow is too weak.
- Parse Jupiter quote `routePlan` to estimate `base_amm_liquidity_share` and dynamic-liquidity dependence.
- Penalize TREND setups whose exit path depends too heavily on dynamic liquidity.
- Keep the implementation deterministic and replay-friendly.

## Definition of done
- Route analyzer works on plain quote JSON.
- Quality multiplier can fully zero noisy orderflow.
- TREND scoring is meaningfully reduced when route quality is fragile.
- Unit tests cover route parsing and scoring effects.

## Tests
- organic_taker_volume_ratio < 0.5 => zero score
- base_amm_liquidity_share < 0.3 => TREND multiplier reduced
- mixed Jupiter route returns sensible base/dynamic shares
