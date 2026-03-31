# PR-015-DIP-REGIME-AND-EXIT-MANAGER-1

## Goal
Add a pullback entry regime (`DIP`) and realistic bootstrap exit logic so replay / paper trade outcomes depend on both entry and exit discipline.

## Files
- `src/strategy/types.py`
- `src/strategy/regime_classifier.py`
- `src/strategy/scoring_v2.py`
- `src/strategy/exit_manager.py`
- `tests/test_strategy_upgrade_v2.py`
- `docs/EXECUTION_AND_EXIT_UPGRADES.md`

## Exact fixes
- Add `price_drop_from_ath_pct` and `smart_wallet_netflow_during_dip_usd`.
- Route healthy pullbacks into a `DIP` regime.
- Add time-stop and momentum-decay exits.
- Use `smart_money_distribution_rate` and `jupiter_sell_impact_bps` as panic-exit conditions.

## Definition of done
- Classifier can return `DIP`.
- `DynamicExitManager` exists with deterministic rules.
- Tests cover DIP classification and exit triggers.

## Tests
- DIP regime classification
- scalp time-stop exit
- smart-money-distribution forced exit
