from src.strategy.execution_gates import TinyCapitalRiskGates
from src.strategy.regime_classifier import RegimeClassifier
from src.strategy.types import CandidateSnapshot


def make_candidate(**overrides):
    candidate = CandidateSnapshot(
        token_address="So11111111111111111111111111111111111111112",
        symbol="TEST",
        liquidity_usd=12000.0,
        jupiter_price_impact_bps=12.0,
        jupiter_sell_impact_bps=18.0,
        rugcheck_status="good",
        mean_volume_5m_per_min_usd=250.0,
        pair_age_seconds=200000,
        taker_buy_volume_usd=2000.0,
        taker_sell_volume_usd=1000.0,
        freshness_age_seconds=60,
        wallet_cohort_score=0.7,
        smart_wallet_coord_score=0.5,
        accumulation_conviction=0.55,
        holder_growth_24h_pct=15.0,
        volume_15m_sustained_multiple=1.8,
        distance_from_smart_entry_pct=0.2,
    )
    for key, value in overrides.items():
        setattr(candidate, key, value)
    return candidate


def test_old_inactive_token_is_filtered_as_zombie():
    c = make_candidate(mean_volume_5m_per_min_usd=8.0, pair_age_seconds=300000)
    decision = RegimeClassifier().classify(c)
    assert decision.regime == "IGNORE"
    assert decision.reason == "zombie_token_inactive_baseline"


def test_active_old_token_still_classifies():
    c = make_candidate(mean_volume_5m_per_min_usd=350.0, pair_age_seconds=300000)
    decision = RegimeClassifier().classify(c)
    assert decision.regime in {"SCALP", "TREND", "DIP"}


def test_eoa_concentration_gate_differs_from_lp_heavy_top_wallet():
    c = make_candidate(
        top_wallet_concentration=0.88,
        eoa_wallet_concentration=0.22,
    )
    gate = TinyCapitalRiskGates().evaluate(c, regime="TREND")
    assert gate.allowed is True
