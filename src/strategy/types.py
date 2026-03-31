from dataclasses import dataclass


@dataclass(slots=True)
class CandidateSnapshot:
    token_address: str
    symbol: str = "UNKNOWN"

    # Legacy aggregate volume view
    volume_5m_usd: float = 0.0
    mean_volume_1h_usd: float = 0.0
    std_volume_1h_usd: float = 1.0

    # Preferred microstructure view for fast Solana tokens
    volume_1m_usd: float = 0.0
    mean_volume_5m_per_min_usd: float = 0.0
    std_volume_5m_per_min_usd: float = 1.0

    # Coarse trade counts
    buys_5m: int = 0
    sells_5m: int = 0

    # Better orderflow features
    taker_buy_volume_usd: float = 0.0
    taker_sell_volume_usd: float = 0.0
    volume_authenticity_ratio: float = 1.0
    organic_taker_volume_ratio: float = 1.0

    # Liquidity and execution
    liquidity_usd: float = 0.0
    jupiter_price_impact_bps: float = 0.0
    jupiter_sell_impact_bps: float = 0.0
    estimated_priority_fee_lamports: int = 0
    local_pool_p75_priority_fee_lamports: int = 0
    estimated_total_fee_sol: float = 0.0
    round_trip_fee_sol: float = 0.0
    jito_tip_hurdle_sol: float = 0.0
    freshness_age_seconds: int = 999999
    pair_age_seconds: int = 0
    amm_reserve_drift_ratio: float = 0.0
    base_amm_liquidity_share: float = 1.0
    route_uses_dynamic_liquidity_share: float = 0.0
    estimated_exit_fee_sol: float = 0.0
    dynamic_liquidity_stress: float = 0.0

    # Safety / anti-rug / anti-manipulation
    rugcheck_status: str = "unknown"
    rugcheck_risk_score: int = 0
    has_socials: bool = False
    mint_authority_present: bool = False
    freeze_authority_present: bool = False
    transfer_hook_present: bool = False
    token2022_transfer_fee_bps: float = 0.0
    token2022_default_frozen: bool = False
    sybil_cluster_share_pct: float = 0.0
    block_0_snipe_pct: float = 0.0
    lp_burn_ratio_pct: float = 100.0

    # Holder / wallet intelligence
    top_wallet_concentration: float = 0.0
    # Concentration across externally owned addresses (EOA) only.
    # Excludes pool/PDA/system vault addresses to avoid false whale concentration.
    eoa_wallet_concentration: float = 0.0
    wallet_cohort_score: float = 0.0
    smart_wallet_coord_score: float = 0.0
    accumulation_conviction: float = 0.0
    holder_growth_24h_pct: float = 0.0
    distance_from_smart_entry_pct: float = 0.0
    smart_money_reference_pnl_pct: float = 0.0
    signed_buy_ratio: float = 1.0

    # Regime context
    oracle_divergence_bps: float = 0.0
    volume_15m_sustained_multiple: float = 0.0
    price_drop_from_ath_pct: float = 0.0
    smart_wallet_netflow_during_dip_usd: float = 0.0
    sol_15m_trend_bps: float = 0.0

    # Exit and replay realism
    smart_money_distribution_rate: float = 0.0
    volume_decay_z: float = 0.0
