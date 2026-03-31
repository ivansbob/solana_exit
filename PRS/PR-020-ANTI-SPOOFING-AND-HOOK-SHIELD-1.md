# PR-020: ANTI-SPOOFING-AND-HOOK-SHIELD-1

## Goal
Prevent smart-money graph poisoning and block Token-2022 transfer-hook exposure in the bootstrap default path.

## Files
- `queries/dune/signed_buy_verification.sql`
- `src/strategy/types.py`
- `src/strategy/execution_gates.py`
- `tests/test_execution_gates.py`
- `docs/ABYSSAL_ZONE_UPGRADES.md`

## Exact fixes
- Add `signed_buy_ratio` to the contract for wallet-cohort trust.
- Add `transfer_hook_present` to the contract and hard-block it by default.
- Reject wallet-signal candidates whose smart-money state is not signer-verified.
- Keep all thresholds configurable and explicitly label them as replay defaults.

## Definition of done
- Dune scaffold exists for signer-only smart-money verification.
- Gates can reject unverified wallet-cohort signals.
- Gates can reject Transfer Hook exposure.

## Tests
- transfer_hook_present => blocked
- signed_buy_ratio < configured minimum and wallet scores > 0 => blocked
