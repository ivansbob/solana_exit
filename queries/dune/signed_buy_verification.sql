-- PR-020 bootstrap stub
-- Goal: verify that "smart money" signals are based on paid buys where the
-- tracked wallet signed a swap-like transaction, not on passive airdrops.
--
-- Expected downstream output fields:
--   wallet_address
--   token_address
--   first_seen_at
--   signed_buy_count
--   passive_transfer_count
--   signed_buy_ratio
--
-- Notes:
-- 1. This is intentionally a scaffold. The exact table set depends on the
--    current Dune Solana decoded coverage available to the project account.
-- 2. We treat signer-verified paid buys as high-trust and passive inbound
--    transfers as low-trust.
-- 3. The final PR should join swap instructions + token transfers and compute
--    a per-wallet/token signed_buy_ratio for the recent lookback window.

WITH candidate_wallet_transfers AS (
    SELECT
        CAST(NULL AS VARCHAR) AS wallet_address,
        CAST(NULL AS VARCHAR) AS token_address,
        CAST(NULL AS TIMESTAMP) AS first_seen_at,
        CAST(NULL AS BIGINT) AS signed_buy_count,
        CAST(NULL AS BIGINT) AS passive_transfer_count
    WHERE 1 = 0
)
SELECT
    wallet_address,
    token_address,
    first_seen_at,
    signed_buy_count,
    passive_transfer_count,
    CASE
        WHEN COALESCE(signed_buy_count, 0) + COALESCE(passive_transfer_count, 0) = 0 THEN NULL
        ELSE CAST(signed_buy_count AS DOUBLE)
            / CAST((signed_buy_count + passive_transfer_count) AS DOUBLE)
    END AS signed_buy_ratio
FROM candidate_wallet_transfers;
