# PR-023: MATH-BOUNDARIES-AND-ZOMBIE-FILTER-1

## Goal
Fix weak mathematical boundaries in scoring and regime selection so low-variance noise and dead-token spikes do not look like high-quality opportunities.

## Files
- `src/strategy/scoring_v2.py`
- `src/strategy/regime_classifier.py`
- `src/strategy/execution_gates.py`
- `src/strategy/types.py`
- `tests/test_scoring_v2.py`
- `tests/test_regime_classifier.py`
- `docs/MATH_BOUNDARIES_AND_ZOMBIE_FILTER.md`

## Exact fixes
- Add a dynamic denominator floor for micro-volume z-score based on pool liquidity.
- Block zombie-token setups where pool age is high but baseline activity is effectively dead.
- Clarify concentration semantics by using EOA concentration instead of naive top-wallet concentration.
- Keep scorer explainability intact for blocked and down-weighted candidates.

## Definition of done
- Low-variance / low-liquidity pools no longer max out z-score on trivial noise.
- Zombie pumps are rejected explicitly.
- EOA-vs-PDA/system concentration semantics are documented and used in the right gates.
- Tests pass.

## Tests
- tiny noisy pool no longer gets max z-score from a trivial spike
- old inactive token is ignored as zombie
- active token still passes
- EOA concentration behaves differently from LP-heavy concentration
