from dataclasses import dataclass

from src.strategy.types import CandidateSnapshot


@dataclass(slots=True)
class RegimeDecision:
    regime: str
    confidence: float
    reason: str


class RegimeClassifier:
    def __init__(
        self,
        *,
        zombie_min_pool_age_seconds: int = 86400,
        zombie_max_baseline_volume_1m_usd: float = 25.0,
    ) -> None:
        self.zombie_min_pool_age_seconds = zombie_min_pool_age_seconds
        self.zombie_max_baseline_volume_1m_usd = zombie_max_baseline_volume_1m_usd

    def classify(self, c: CandidateSnapshot) -> RegimeDecision:
        if c.jupiter_price_impact_bps > 40 or c.liquidity_usd < 8000:
            return RegimeDecision("IGNORE", 0.95, "execution_unfriendly")
        if c.rugcheck_status.lower() in {"danger", "scam"}:
            return RegimeDecision("IGNORE", 0.99, "anti_rug_failed")
        if self._is_zombie_token(c):
            return RegimeDecision("IGNORE", 0.97, "zombie_token_inactive_baseline")

        macro_risk = c.sol_15m_trend_bps < -50

        dip_conditions = [
            c.wallet_cohort_score >= 0.60,
            0.15 <= c.price_drop_from_ath_pct <= 0.40,
            c.smart_wallet_netflow_during_dip_usd > 0,
            c.taker_buy_volume_usd > c.taker_sell_volume_usd * 1.10,
            c.jupiter_price_impact_bps <= 20,
        ]
        dip_hits = sum(bool(x) for x in dip_conditions)
        if dip_hits >= 4:
            return RegimeDecision("DIP", 0.63 + 0.06 * dip_hits, "smart_money_buying_the_dip")

        scalp_conditions = [
            c.volume_1m_usd > max(c.mean_volume_5m_per_min_usd, 1.0) * 1.8,
            c.taker_buy_volume_usd > c.taker_sell_volume_usd * 1.8,
            c.jupiter_price_impact_bps <= 25,
            c.freshness_age_seconds <= 90,
            c.volume_authenticity_ratio >= 0.50,
            c.pair_age_seconds >= 300,
        ]
        scalp_hits = sum(bool(x) for x in scalp_conditions)
        if not macro_risk and scalp_hits >= 4:
            return RegimeDecision("SCALP", 0.62 + 0.05 * scalp_hits, "fast_orderflow_breakout")

        trend_conditions = [
            c.wallet_cohort_score >= 0.55,
            c.smart_wallet_coord_score >= 0.40,
            c.accumulation_conviction >= 0.35,
            c.holder_growth_24h_pct >= 10.0,
            c.volume_15m_sustained_multiple >= 1.5,
            c.distance_from_smart_entry_pct <= 0.40,
        ]
        trend_hits = sum(bool(x) for x in trend_conditions)
        if trend_hits >= 4:
            confidence = 0.60 + 0.05 * trend_hits
            if macro_risk:
                confidence -= 0.05
            return RegimeDecision("TREND", confidence, "sustained_follow_through")

        return RegimeDecision("IGNORE", 0.80, "insufficient_edge")

    def _is_zombie_token(self, c: CandidateSnapshot) -> bool:
        baseline_1m = c.mean_volume_5m_per_min_usd or (c.mean_volume_1h_usd / 60.0)
        return c.pair_age_seconds >= self.zombie_min_pool_age_seconds and baseline_1m <= self.zombie_max_baseline_volume_1m_usd
