# EXIT REALISM AND HARD STOPS

This planned upgrade makes exit decisions depend on executable net economics rather than naive mark-to-market PnL.

Planned additions:
- net executable PnL helper
- hard stop-loss for tiny-capital protection
- dynamic-liquidity haircut on optimistic profit assumptions
- more defensive logic when reference smart-money cohorts are deeply underwater

Design principle:
A paper-trade exit is only counted as good if it is plausibly executable after sell impact and fee drag.
