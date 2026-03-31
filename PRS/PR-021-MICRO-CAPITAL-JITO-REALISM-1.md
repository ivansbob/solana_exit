# PR-021: MICRO-CAPITAL-JITO-REALISM-1

## Goal
Reflect the fact that tiny-capital execution can be dominated by tip overhead and landing competition during hot moments.

## Files
- `src/strategy/types.py`
- `src/strategy/scoring_v2.py`
- `src/paper/mev_simulator.py`
- `tests/test_mev_simulator.py`
- `docs/ABYSSAL_ZONE_UPGRADES.md`

## Exact fixes
- Add `jito_tip_hurdle_sol` to the contract.
- Penalize setups whose move profile is too small to overcome tiny-capital landing overhead.
- Keep this logic off the critical path for cold/slow setups but material for hot SCALP conditions.
- Document the distinction between chain fees, priority fees, and tip hurdles.

## Definition of done
- Scoring penalizes expensive tiny-capital routing.
- Simulator carries fee drag explicitly.
- Tests show increased drag in contested regimes.

## Tests
- high jito_tip_hurdle_sol => higher exec cost penalty
- contested SCALP + small sustained move => worse total score
