# EXECUTION_AND_EXIT_UPGRADES

## New execution realism ideas in the bootstrap
- Buy-side impact and sell-side impact are checked separately.
- Round-trip fee is treated as a first-class cost.
- Sell/buy impact asymmetry can block a trade entirely.

## New exit logic
`src/strategy/exit_manager.py` introduces a pragmatic bootstrap exit layer for replay and paper trade:
- panic exit if smart money starts distributing
- panic exit if sell impact explodes
- `SCALP` time-stop if momentum never follows through
- partial exits on momentum decay

## Why this matters
A paper-trade system without exits can overstate edge.
For tiny-capital Solana setups, realized expectancy is often driven as much by exit discipline as by entry quality.
