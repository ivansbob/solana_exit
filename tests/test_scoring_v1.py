from src.strategy.execution_gates import TinyCapitalRiskGates
from src.strategy.regime_classifier import RegimeClassifier
from src.strategy.scoring_v1 import OpportunityScorer
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
        liquidity_usd=14200,
        top_wallet_concentration=0.28,
        wallet_cohort_score=0.74,
        smart_wallet_coord_score=0.58,
        accumulation_conviction=0.78,
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
        distance_from_smart_entry_pct=0.12,
    )
    for k, v in overrides.items():
        setattr(base, k, v)
    return base


def test_gates_pass():
    assert TinyCapitalRiskGates().evaluate(make_candidate()).allowed is True


def test_gates_reject_impact():
    d = TinyCapitalRiskGates().evaluate(make_candidate(jupiter_price_impact_bps=55))
    assert d.allowed is False and d.reason == "price_impact_too_high"


def test_classifier_not_ignore_for_good_candidate():
    assert RegimeClassifier().classify(make_candidate(price_drop_from_ath_pct=0.0, smart_wallet_netflow_during_dip_usd=0.0)).regime in {"SCALP", "TREND"}


def test_classifier_ignore_bad_liquidity():
    assert RegimeClassifier().classify(make_candidate(liquidity_usd=5000)).regime == "IGNORE"


def test_trend_score_can_pass():
    r = OpportunityScorer().score(make_candidate(), "TREND")
    assert r.total_score > r.threshold and r.entry_allowed is True


def test_high_impact_penalized():
    r = OpportunityScorer().score(make_candidate(jupiter_price_impact_bps=95), "TREND")
    assert r.exec_cost_penalty > 0 and r.total_score < 1.45


def test_ignore_has_zero_score():
    r = OpportunityScorer().score(make_candidate(), "IGNORE")
    assert r.total_score == 0.0 and r.entry_allowed is False
