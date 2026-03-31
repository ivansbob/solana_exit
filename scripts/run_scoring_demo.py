from src.strategy.execution_gates import TinyCapitalRiskGates
from src.strategy.exit_manager import DynamicExitManager, PositionState
from src.strategy.regime_classifier import RegimeClassifier
from src.strategy.scoring_v2 import OpportunityScorerV2
from src.strategy.types import CandidateSnapshot


candidate = CandidateSnapshot(
    token_address="So11111111111111111111111111111111111111112",
    symbol="DEMO",
    volume_5m_usd=45000,
    mean_volume_1h_usd=8000,
    std_volume_1h_usd=6000,
    volume_1m_usd=16000,
    mean_volume_5m_per_min_usd=4000,
    std_volume_5m_per_min_usd=2500,
    buys_5m=142,
    sells_5m=31,
    taker_buy_volume_usd=24000,
    taker_sell_volume_usd=7000,
    volume_authenticity_ratio=0.72,
    liquidity_usd=14200,
    top_wallet_concentration=0.28,
    wallet_cohort_score=0.68,
    smart_wallet_coord_score=0.51,
    accumulation_conviction=0.61,
    oracle_divergence_bps=22,
    jupiter_price_impact_bps=22,
    jupiter_sell_impact_bps=28,
    estimated_priority_fee_lamports=4000,
    estimated_total_fee_sol=0.00012,
    round_trip_fee_sol=0.00028,
    freshness_age_seconds=45,
    pair_age_seconds=900,
    rugcheck_status="good",
    rugcheck_risk_score=1200,
    has_socials=True,
    lp_burn_ratio_pct=100.0,
    holder_growth_24h_pct=16.0,
    volume_15m_sustained_multiple=1.9,
    price_drop_from_ath_pct=0.22,
    smart_wallet_netflow_during_dip_usd=6800,
    sol_15m_trend_bps=18,
    distance_from_smart_entry_pct=0.12,
)

gate_decision = TinyCapitalRiskGates().evaluate(candidate)
print("gate_decision=", gate_decision)
if gate_decision.allowed:
    regime = RegimeClassifier().classify(candidate)
    print("regime=", regime)
    score = OpportunityScorerV2().score(candidate, regime.regime)
    print("score=", score)
    position = PositionState(regime=regime.regime, age_seconds=240, unrealized_pnl_pct=0.11)
    exit_decision = DynamicExitManager().evaluate(position, candidate)
    print("exit_decision=", exit_decision)
