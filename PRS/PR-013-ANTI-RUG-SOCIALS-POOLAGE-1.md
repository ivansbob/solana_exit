# PR-013-ANTI-RUG-SOCIALS-POOLAGE-1

## Goal
Add a free-first anti-rug and token-context layer before opportunity scoring so the engine can reject obvious scam tokens, too-young pools, and blind/no-context setups before paper entries are considered.

## Why now
The current bootstrap is strong on tiny-capital execution realism and regime routing, but it is still under-protected against avoidable token-level blowups. For $5-sized paper trading, avoiding bad trades matters more than widening coverage. This PR adds the cheapest, highest-leverage filters first.

## Primary sources to integrate
- RugCheck token report adapter for normalized anti-rug context
- DexScreener token/pair context for socials and pair age

## Files
- `src/ingest/rugcheck_adapter.py`
- `src/ingest/dexscreener_token_context.py`
- `src/strategy/types.py`
- `src/strategy/execution_gates.py`
- `tests/test_rugcheck_adapter.py`
- `tests/test_execution_gates.py`
- `docs/ANTI_RUG_AND_CONTEXT.md`
- `data_contracts/candidate_snapshot.schema.json`

## Exact fixes
1. Add a normalized RugCheck adapter that returns a stable machine-readable object with at least:
   - `rugcheck_status`
   - `rugcheck_score`
   - `mint_authority_present`
   - `freeze_authority_present`
   - `is_token_2022` when detectable
   - `risk_flags` as a string list
2. Add a DexScreener context adapter that returns at least:
   - `has_socials`
   - `pair_age_seconds`
   - `dex_pair_created_at_ms`
3. Extend `CandidateSnapshot` with the new fields above.
4. Update `execution_gates.py` so hard gates are checked before score-based entry logic:
   - block explicit RugCheck danger/scam states
   - block open mint authority
   - block open freeze authority
   - block breakout/scalp-style entries for pools younger than the configured threshold
   - do **not** treat socials as a hard positive signal; use missing socials only as a negative context signal for non-brand-new tokens
5. Make every anti-rug rejection reason explicit and machine-readable.
6. Add config-friendly thresholds and defaults; do not hard-code magic numbers without named constants.
7. Update schema/docs so these fields are visible in replay artifacts and future reports.

## Definition of done
- Candidate snapshots can carry anti-rug and token-context fields end-to-end
- execution gates can reject a candidate with explicit reasons such as:
  - `rugcheck_status_danger`
  - `mint_authority_present`
  - `freeze_authority_present`
  - `pool_too_young_for_scalp`
  - `no_socials_on_non_new_token`
- tests cover safe path and rejection path
- docs clearly state that thresholds are replay-calibration defaults, not universal truths

## Tests
- danger token -> blocked
- token with mint authority -> blocked
- token with freeze authority -> blocked
- young pool + scalp/trend breakout context -> blocked
- older token with no socials -> penalized or blocked according to config
- safe token with socials and mature pair -> allowed

## Notes for Codex
- Keep the adapter interface lightweight and deterministic
- Prefer explainable booleans and flags over a single opaque risk score
- Do not add live auto-execution or trade sending
- Preserve free-first assumptions and graceful degradation when external APIs are unavailable
