SELECT
  trader_id,
  COUNT(*) AS total_entries
FROM dex_solana.trades
WHERE block_time >= NOW() - INTERVAL '90' DAY
GROUP BY 1
HAVING COUNT(*) >= 8
ORDER BY total_entries DESC
LIMIT 5000;
