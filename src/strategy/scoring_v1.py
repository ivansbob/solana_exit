from dataclasses import dataclass
from src.strategy.types import CandidateSnapshot

@dataclass(slots=True)
class ScoreBreakdown:
    regime: str
    total_score: float
    vol_accel_z: float
    imbalance_norm: float
    liq_stability: float
    concentration_penalty: float
    oracle_divergence_score: float
    freshness_bonus: float
    exec_cost_penalty: float
    wallet_cohort_score: float
    smart_wallet_coord_score: float
    accumulation_conviction: float
    entry_allowed: bool
    threshold: float

class OpportunityScorer:
    SCALP_THRESHOLD = 1.35
    TREND_THRESHOLD = 1.45

    def score(self, c: CandidateSnapshot, regime: str) -> ScoreBreakdown:
        vol_accel_z = self._vol_accel_z(c)
        imbalance_norm = self._imbalance_norm(c)
        liq_stability = self._liq_stability(c)
        concentration_penalty = self._concentration_penalty(c)
        oracle_divergence_score = self._oracle_divergence_score(c)
        freshness_bonus = self._freshness_bonus(c)
        exec_cost_penalty = self._exec_cost_penalty(c)
        if regime == "SCALP":
            total_score = (
                0.42 * vol_accel_z + 0.18 * imbalance_norm + 0.10 * c.wallet_cohort_score +
                0.08 * c.smart_wallet_coord_score + 0.06 * liq_stability + 0.04 * oracle_divergence_score +
                0.03 * freshness_bonus - 0.04 * concentration_penalty - exec_cost_penalty
            )
            threshold = self.SCALP_THRESHOLD
        elif regime == "TREND":
            total_score = (
                0.32 * vol_accel_z + 0.14 * imbalance_norm + 0.20 * c.wallet_cohort_score +
                0.12 * c.smart_wallet_coord_score + 0.10 * c.accumulation_conviction + 0.06 * liq_stability +
                0.04 * oracle_divergence_score + 0.03 * freshness_bonus -
                0.05 * concentration_penalty - exec_cost_penalty
            )
            threshold = self.TREND_THRESHOLD
        else:
            total_score = 0.0
            threshold = 999.0
        return ScoreBreakdown(
            regime=regime, total_score=round(total_score, 6), vol_accel_z=round(vol_accel_z, 6),
            imbalance_norm=round(imbalance_norm, 6), liq_stability=round(liq_stability, 6),
            concentration_penalty=round(concentration_penalty, 6),
            oracle_divergence_score=round(oracle_divergence_score, 6),
            freshness_bonus=round(freshness_bonus, 6), exec_cost_penalty=round(exec_cost_penalty, 6),
            wallet_cohort_score=round(c.wallet_cohort_score, 6),
            smart_wallet_coord_score=round(c.smart_wallet_coord_score, 6),
            accumulation_conviction=round(c.accumulation_conviction, 6),
            entry_allowed=bool(total_score > threshold), threshold=threshold,
        )

    def _vol_accel_z(self, c: CandidateSnapshot) -> float:
        denom = c.std_volume_1h_usd if c.std_volume_1h_usd > 0 else 1.0
        z = (c.volume_5m_usd - c.mean_volume_1h_usd) / denom
        if z < 0:
            return 0.0
        return min(3.0, z)

    def _imbalance_norm(self, c: CandidateSnapshot) -> float:
        raw = (max(0, c.buys_5m) - max(0, c.sells_5m)) / (max(0, c.buys_5m) + max(0, c.sells_5m) + 1)
        return max(0.0, min(1.0, raw))

    def _liq_stability(self, c: CandidateSnapshot) -> float:
        if c.liquidity_usd >= 12000:
            return 1.0
        if c.liquidity_usd >= 8000:
            return 0.5
        return 0.0

    def _concentration_penalty(self, c: CandidateSnapshot) -> float:
        return max(0.0, c.top_wallet_concentration - 0.35) * 3.0

    def _oracle_divergence_score(self, c: CandidateSnapshot) -> float:
        bps = abs(c.oracle_divergence_bps)
        if 20 <= bps <= 80:
            return 1.0
        if 10 < bps < 20:
            return 0.5
        return 0.0

    def _freshness_bonus(self, c: CandidateSnapshot) -> float:
        age = max(0, c.freshness_age_seconds)
        if age < 180:
            return 0.6
        if age < 480:
            return 0.3
        return 0.0

    def _exec_cost_penalty(self, c: CandidateSnapshot) -> float:
        impact_bps = max(0.0, c.jupiter_price_impact_bps)
        if impact_bps <= 35:
            penalty = 0.0
        elif impact_bps <= 100:
            penalty = (impact_bps - 35) / 110.0
        else:
            penalty = 3.0
        if c.estimated_priority_fee_lamports > 8000:
            penalty += 0.1
        return penalty
