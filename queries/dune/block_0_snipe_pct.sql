-- PR-016 scaffold
-- Goal: estimate how much supply was accumulated in the first tradable block / launch window.
-- Replace placeholder source tables with the project's chosen curated Solana trade tables.

WITH launch_trades AS (
    SELECT
        token_address,
        block_time,
        trader,
        amount_token
    FROM some_solana_trade_table
    WHERE token_address = :token_address
),
first_window AS (
    SELECT *
    FROM launch_trades
    WHERE block_time <= (SELECT MIN(block_time) + INTERVAL '5 second' FROM launch_trades)
)
SELECT
    token_address,
    SUM(amount_token) AS launch_window_amount_token
FROM first_window
GROUP BY 1;
