from src.paper.mev_simulator import BootstrapMEVSimulator
from src.strategy.execution_gates import TinyCapitalRiskGates
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
        organic_taker_volume_ratio=0.81,
        liquidity_usd=14200,
        jupiter_price_impact_bps=22,
        jupiter_sell_impact_bps=28,
        estimated_priority_fee_lamports=4000,
        local_pool_p75_priority_fee_lamports=9000,
        estimated_total_fee_sol=0.00012,
        round_trip_fee_sol=0.00028,
        jito_tip_hurdle_sol=0.0004,
        freshness_age_seconds=45,
        pair_age_seconds=900,
        amm_reserve_drift_ratio=0.003,
        base_amm_liquidity_share=0.65,
        route_uses_dynamic_liquidity_share=0.20,
        rugcheck_status="good",
        rugcheck_risk_score=1200,
        has_socials=True,
        mint_authority_present=False,
        freeze_authority_present=False,
        transfer_hook_present=False,
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
        signed_buy_ratio=1.0,
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


def test_gate_rejects_transfer_hook_present():
    d = TinyCapitalRiskGates().evaluate(make_candidate(transfer_hook_present=True))
    assert d.allowed is False and d.reason == "token2022_transfer_hook_present"


def test_gate_rejects_unsigned_smart_money_signal():
    d = TinyCapitalRiskGates().evaluate(make_candidate(signed_buy_ratio=0.70))
    assert d.allowed is False and d.reason == "smart_money_not_signed_buy_verified"


def test_gate_rejects_large_amm_drift():
    d = TinyCapitalRiskGates().evaluate(make_candidate(amm_reserve_drift_ratio=0.05))
    assert d.allowed is False and d.reason == "amm_reserve_drift_too_high"


def test_v2_score_zeroes_non_organic_orderflow():
    r = OpportunityScorerV2().score(make_candidate(organic_taker_volume_ratio=0.20), "DIP")
    assert r.quality_multiplier == 0.0 and r.total_score == 0.0


def test_v2_score_penalizes_jito_hurdle_on_scalp():
    fast = OpportunityScorerV2().score(make_candidate(jito_tip_hurdle_sol=0.0016), "SCALP")
    cheap = OpportunityScorerV2().score(make_candidate(jito_tip_hurdle_sol=0.0002), "SCALP")
    assert fast.exec_cost_penalty > cheap.exec_cost_penalty
    assert fast.total_score < cheap.total_score


def test_mev_simulator_applies_adverse_selection_and_fee_drag():
    sim = BootstrapMEVSimulator().simulate(
        vol_accel_z=2.8,
        sell_impact_bps=30,
        next_return_pct=0.20,
        jito_tip_hurdle_sol=0.0015,
        local_pool_priority_fee_lamports=20000,
        amm_reserve_drift_ratio=0.03,
    )
    assert sim.failed_fill_probability > 0.35
    assert sim.base_fee_drag_sol == 0.0015
    assert sim.failed_attempt_fee_drag_sol > 0.0
    assert sim.fee_drag_sol > sim.base_fee_drag_sol
    assert sim.status_bias in {"ADVERSE_SELECTION_UP", "CACHE_LAG_RISK", "MEV_CONTESTED"}
