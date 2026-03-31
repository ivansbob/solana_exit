# MATH BOUNDARIES AND ZOMBIE FILTER

This planned upgrade strengthens two weak spots:
- over-reactive micro-volume z-scores in low-variance pools
- false-positive momentum on very old, inactive pools

Planned additions:
- liquidity-aware denominator floors for micro z-score
- zombie-token filter based on pool age and baseline activity
- explicit EOA concentration semantics so LP/PDA/system accounts are not misread as whale concentration
