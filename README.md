# solana-papertrade-edge-free-bootstrap

Free-first bootstrap repository for **Solana paper trading, historical replay, and shadow/manual signals** with a tiny-capital mindset.

## Objective
Increase the quality of simulated paper trades by combining:
- deterministic scoring formulas
- hard execution gates for tiny position sizes
- regime split (`SCALP`, `TREND`, `DIP`, `IGNORE`)
- historical replay
- ablation + calibration before any live/manual deployment
- realistic exit simulation and round-trip execution checks

## What this repo is
This is **not** an auto-profit bot.
It is a research-first system that helps you test whether a setup still has positive expectancy after:
- slippage
- asymmetric buy/sell impact
- base fees / priority fees
- stale data penalties
- liquidity filters
- concentration risk
- anti-rug / anti-manipulation gates
- time-stop and momentum-decay exits

## Recommended free-first stack
- Dune Free
- Helius Free
- DexScreener
- GeckoTerminal
- Jupiter
- Pyth Hermes
- Drift Data API
- DefiLlama Free API
- RugCheck API

## Current practical focus
The current bootstrap is optimized for:
- **tiny-capital paper trading**
- **SCALP vs TREND vs DIP** routing
- **anti-rug and anti-manipulation filtering**
- **replay-ready scoring and exits**

## Immediate next steps
1. Finish / review `PR-013-ANTI-RUG-SOCIALS-POOLAGE-1`
2. Give Codex `CODEX_PROMPTS/PR-014.txt`
3. After PR-014, continue with `CODEX_PROMPTS/PR-015.txt`
