# MICROSTRUCTURE AND OVERHANG SHIELD

This upgrade adds two conservative protections:
- dynamic-liquidity exit optimism haircut
- retained early-buyer overhang tracking

Implemented additions:
- `upside_liquidity_density` for dynamic-route upside depth realism
- `sleeping_sniper_overhang_pct` and `sleeping_sniper_unrealized_gain_pct`
- extra executable-PnL haircuts when dynamic routes have thin upside density
- defensive penalty when retained early-buyer overhang and unrealized gains are both dangerous
- missing-data honesty penalty on high dynamic-route exits when overhang inputs are unknown
- Dune placeholder query for retained early-buyer overhang research

Design principle:
Missing overhang data must remain explicitly unknown rather than being silently treated as safe.
