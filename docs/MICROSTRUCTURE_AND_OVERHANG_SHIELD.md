# MICROSTRUCTURE AND OVERHANG SHIELD

This planned upgrade adds two conservative protections:
- dynamic-liquidity exit optimism haircut
- retained early-buyer overhang tracking

Planned additions:
- fields for sleeping-sniper overhang and unrealized gain overhang
- defensive exit logic when dynamic-liquidity routes dominate
- research query placeholder for retained early-buyer supply overhang

Design principle:
Missing overhang data must remain explicitly unknown rather than being silently treated as safe.
