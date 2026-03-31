# PR-027: FUNDING-ENTROPY-AND-MEV-VOLUME-STRIP-1

## Goal
Strengthen smart-money and orderflow quality by filtering sybil-like coordinated funding and stripping MEV/arb-distorted volume from the scoring baseline.

## Files
- `queries/dune/funding_source_entropy.sql`
- `queries/dune/mev_stripped_volume.sql`
- `src/strategy/execution_gates.py`
- `src/strategy/scoring_v2.py`
- `src/strategy/types.py`
- `tests/test_abyssal_upgrades.py`
- `docs/FUNDING_ENTROPY_AND_MEV_VOLUME_STRIP.md`

## Exact fixes
- Add funding-source entropy and shared-funder cluster fields.
- Distinguish organic taker volume from MEV-distorted or atomic-arb-heavy flow.
- Penalize or block candidates where coordinated wallet activity comes from a low-entropy funding graph.
- Use MEV-stripped volume in score-critical calculations when available.
- Preserve missing-data honesty: unknown is not automatically safe.

## Definition of done
- Smart-money quality is less vulnerable to sybil funding spoofing.
- Volume scoring is less vulnerable to sandwich/arbitrage noise.
- Tests and docs reflect the new semantics.

## Tests
- low funding entropy => gate penalty or block
- high shared-funder cluster ratio => lower candidate quality
- organic volume below threshold => score suppressed
- missing MEV-strip data handled honestly
