SELECT
  block_time,
  tx_id,
  trader_id,
  token_bought_mint_address AS token_address,
  amount_usd
FROM dex_solana.trades
WHERE block_time >= NOW() - INTERVAL '1' DAY
  AND amount_usd IS NOT NULL
ORDER BY block_time DESC
LIMIT 10000;
