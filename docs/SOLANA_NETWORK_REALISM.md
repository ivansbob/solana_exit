# SOLANA NETWORK REALISM

This upgrade makes tiny-capital simulation more pessimistic and more honest for paper/replay mode.

## What is modeled now

- **ATA rent drag on first entry**: first buy can pay associated token account rent when no ATA exists yet.
- **Optional ATA rent reclaim on full exit**: if the strategy assumption is to close the account on full exit, rent can be reclaimed.
- **Failed transaction fee drag**: failed attempts consume base network fee, so retries are not free.
- **Explicit network cost breakdown**: simulator output now splits base fee, MEV tip, failed-attempt drag, ATA rent drag, and optional reclaim.

## Default assumptions (configurable)

- `ata_rent_exempt_sol`: `0.00203928` SOL
- `failed_tx_base_fee_sol` / simulator `base_tx_fee_sol`: `0.000005` SOL
- `assume_no_existing_ata`: `False`
- `reclaim_ata_rent_on_full_exit`: `False`

These defaults are intentionally conservative for tiny-capital replay and can be overridden per scenario.

## Design principle

Failed attempts are not free, and tiny-capital paper trading should model that explicitly.
