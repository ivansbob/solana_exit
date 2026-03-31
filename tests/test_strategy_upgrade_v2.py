from src.strategy.execution_gates import TinyCapitalRiskGates
from src.strategy.exit_manager import DynamicExitManager, PositionState
from src.strategy.regime_classifier import RegimeClassifier
from src.strategy.scoring_v2 import OpportunityScorerV2
from src.strategy.types import CandidateSnapshot


def make_candidate(**overrides):
    base = CandidateSnapshot(
        token_address="So11111111111111111111111111111111111111112",
        symbol="TEST",
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
        mint_authority_present=False,
        freeze_authority_present=False,
        token2022_transfer_fee_bps=0.0,
        token2022_default_frozen=False,
        sybil_cluster_share_pct=8.0,
        block_0_snipe_pct=6.0,
        lp_burn_ratio_pct=100.0,
        top_wallet_concentration=0.28,
        wallet_cohort_score=0.74,
        smart_wallet_coord_score=0.58,
        accumulation_conviction=0.78,
        holder_growth_24h_pct=16.0,
        distance_from_smart_entry_pct=0.12,
        oracle_divergence_bps=22,
        volume_15m_sustained_multiple=1.9,
        price_drop_from_ath_pct=0.22,
        smart_wallet_netflow_during_dip_usd=6800,
        sol_15m_trend_bps=18,
        smart_money_distribution_rate=0.0,
        volume_decay_z=0.2,
    )
    for key, value in overrides.items():
        setattr(base, key, value)
    return base


def test_gates_reject_sell_impact_asymmetry():
    d = TinyCapitalRiskGates().evaluate(make_candidate(jupiter_sell_impact_bps=50, jupiter_price_impact_bps=20))
    assert d.allowed is False and d.reason == "sell_buy_impact_asymmetry_too_high"


def test_gates_reject_sybil_cluster():
    d = TinyCapitalRiskGates().evaluate(make_candidate(sybil_cluster_share_pct=40))
    assert d.allowed is False and d.reason == "sybil_cluster_share_too_high"


def test_regime_prefers_dip_when_pullback_is_clean():
    regime = RegimeClassifier().classify(make_candidate())
    assert regime.regime == "DIP"


def test_regime_blocks_scalp_when_sol_is_weak():
    candidate = make_candidate(
        price_drop_from_ath_pct=0.0,
        smart_wallet_netflow_during_dip_usd=0.0,
        sol_15m_trend_bps=-80,
        taker_buy_volume_usd=30000,
        taker_sell_volume_usd=9000,
        volume_1m_usd=20000,
        freshness_age_seconds=30,
    )
    regime = RegimeClassifier().classify(candidate)
    assert regime.regime != "SCALP"


def test_v2_score_can_pass_for_dip_candidate():
    r = OpportunityScorerV2().score(make_candidate(), "DIP")
    assert r.entry_allowed is True and r.total_score > r.threshold


def test_v2_score_kill_switch_zeroes_bad_authenticity():
    r = OpportunityScorerV2().score(make_candidate(volume_authenticity_ratio=0.10), "DIP")
    assert r.quality_multiplier == 0.0 and r.total_score == 0.0


def test_exit_manager_time_stop_for_failed_scalp():
    position = PositionState(regime="SCALP", age_seconds=220, unrealized_pnl_pct=0.002)
    decision = DynamicExitManager().evaluate(position, make_candidate(price_drop_from_ath_pct=0.0, smart_wallet_netflow_during_dip_usd=0.0))
    assert decision.should_exit is True and decision.reason == "time_stop_no_follow_through"


def test_exit_manager_distribution_forces_exit():
    position = PositionState(regime="TREND", age_seconds=90, unrealized_pnl_pct=0.08)
    decision = DynamicExitManager().evaluate(position, make_candidate(smart_money_distribution_rate=0.50))
    assert decision.should_exit is True and decision.reason == "smart_money_dumping"
