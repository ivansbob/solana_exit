# PR-025: MICROSTRUCTURE-AND-OVERHANG-SHIELD-1

## Goal
Add protection against thin upside liquidity in dynamic-liquidity pools and against dangerous retained supply overhang from very early buyers.

## Files
- `src/strategy/exit_manager.py`
- `src/strategy/types.py`
- `queries/dune/sleeping_sniper_overhang.sql`
- `tests/test_exit_manager.py`
- `docs/MICROSTRUCTURE_AND_OVERHANG_SHIELD.md`

## Exact fixes
- Add fields for sleeping-sniper overhang, unrealized gain overhang, and upside liquidity density.
- Haircut optimistic unrealized PnL for highly dynamic-liquidity exit routes.
- Tighten defensiveness when retained early-buyer supply sits on large unrealized gains.
- Add a Dune research query placeholder for retained early-buyer overhang.
- Preserve missing-data honesty rather than silently treating unknown overhang as safe.

## Definition of done
- Exit realism is stricter for dynamic-liquidity pools.
- Retained early-buyer overhang is represented.
- Missing-data honesty is preserved.
- Tests pass.

## Tests
- dynamic-liquidity exits are haircut conservatively
- dangerous overhang increases defensiveness
- missing overhang data is not silently treated as safe
