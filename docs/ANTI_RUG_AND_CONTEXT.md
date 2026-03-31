# ANTI_RUG_AND_CONTEXT

## Added defaults
The bootstrap now treats these as hard or near-hard blockers before paper-trade entry quality is even considered:
- RugCheck explicit `danger` / `scam` status
- high RugCheck risk score
- open mint authority
- open freeze authority
- Token-2022 transfer fees
- Token-2022 default frozen state
- low LP burn ratio
- pool too young for breakout mode

## Why socials are only a weak context signal
Social presence is useful as a weak context filter for older tokens, but is too easy to fake to serve as a strong positive alpha signal by itself.

## Why pair age matters
Very young pools can show extreme momentum that is mostly launch noise, migration noise, or sniper unwind.
The bootstrap therefore blocks early breakout entries by default and prefers waiting for cleaner structure or a later DIP entry.
