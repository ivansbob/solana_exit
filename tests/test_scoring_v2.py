from src.strategy.scoring_v2 import OpportunityScorerV2
from src.strategy.types import CandidateSnapshot


def make_candidate(**overrides):
    candidate = CandidateSnapshot(
        token_address="So11111111111111111111111111111111111111112",
        symbol="TEST",
        liquidity_usd=10000,
        volume_1m_usd=100.0,
        mean_volume_5m_per_min_usd=95.0,
        std_volume_5m_per_min_usd=0.5,
        mean_volume_1h_usd=5700.0,
        std_volume_1h_usd=30.0,
        taker_buy_volume_usd=200.0,
        taker_sell_volume_usd=100.0,
        volume_authenticity_ratio=0.8,
        organic_taker_volume_ratio=0.8,
        wallet_cohort_score=0.6,
        smart_wallet_coord_score=0.5,
        accumulation_conviction=0.5,
        holder_growth_24h_pct=12.0,
        distance_from_smart_entry_pct=0.1,
        freshness_age_seconds=60,
        jupiter_price_impact_bps=10.0,
        jupiter_sell_impact_bps=15.0,
        top_wallet_concentration=0.25,
        oracle_divergence_bps=25.0,
        pair_age_seconds=1200,
        has_socials=True,
    )
    for key, value in overrides.items():
        setattr(candidate, key, value)
    return candidate


def test_micro_volume_zscore_uses_dynamic_floor_on_tiny_liquidity():
    scorer = OpportunityScorerV2()
    tiny_pool = make_candidate(
        liquidity_usd=900.0,
        volume_1m_usd=102.0,
        mean_volume_5m_per_min_usd=100.0,
        std_volume_5m_per_min_usd=0.01,
    )
    score = scorer.score(tiny_pool, "SCALP")
    assert score.micro_vol_accel_z < 0.3


def test_concentration_penalty_prefers_eoa_semantics_over_top_wallet():
    scorer = OpportunityScorerV2()
    candidate = make_candidate(top_wallet_concentration=0.90, eoa_wallet_concentration=0.20)
    score = scorer.score(candidate, "TREND")
    assert score.concentration_penalty == 0.0
