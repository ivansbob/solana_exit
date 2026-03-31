from dataclasses import dataclass

from src.strategy.types import CandidateSnapshot


@dataclass(slots=True)
class ScoreBreakdownV2:
    regime: str
    total_score: float
    threshold: float
    entry_allowed: bool
    micro_vol_accel_z: float
    taker_imbalance_score: float
    dip_recovery_score: float
    liquidity_safety_score: float
    concentration_penalty: float
    oracle_divergence_score: float
    freshness_bonus: float
    exec_cost_penalty: float
    quality_multiplier: float


class OpportunityScorerV2:
    SCALP_THRESHOLD = 1.30
    TREND_THRESHOLD = 1.40
    DIP_THRESHOLD = 1.18

    def score(self, c: CandidateSnapshot, regime: str) -> ScoreBreakdownV2:
        micro_vol_accel_z = self._micro_vol_accel_z(c)
        taker_imbalance_score = self._taker_imbalance_score(c)
        dip_recovery_score = self._dip_recovery_score(c)
        liquidity_safety_score = self._liquidity_safety_score(c)
        concentration_penalty = self._concentration_penalty(c)
        oracle_divergence_score = self._oracle_divergence_score(c)
        freshness_bonus = self._freshness_bonus(c)
        exec_cost_penalty = self._exec_cost_penalty(c, regime)
        quality_multiplier = self._quality_multiplier(c, regime)

        if regime == "SCALP":
            total = (
                0.34 * micro_vol_accel_z
                + 0.22 * taker_imbalance_score
                + 0.12 * c.wallet_cohort_score
                + 0.08 * c.smart_wallet_coord_score
                + 0.08 * liquidity_safety_score
                + 0.05 * freshness_bonus
                + 0.03 * oracle_divergence_score
                - 0.05 * concentration_penalty
                - exec_cost_penalty
            ) * quality_multiplier
            threshold = self.SCALP_THRESHOLD
        elif regime == "TREND":
            smart_entry_multiplier = self._smart_entry_multiplier(c)
            total = (
                0.18 * micro_vol_accel_z
                + 0.12 * taker_imbalance_score
                + 0.22 * c.wallet_cohort_score
                + 0.14 * c.smart_wallet_coord_score
                + 0.12 * c.accumulation_conviction
                + 0.08 * liquidity_safety_score
                + 0.05 * self._holder_growth_score(c)
                + 0.03 * oracle_divergence_score
                - 0.05 * concentration_penalty
                - exec_cost_penalty
            ) * quality_multiplier * smart_entry_multiplier
            threshold = self.TREND_THRESHOLD
        elif regime == "DIP":
            total = (
                0.18 * micro_vol_accel_z
                + 0.10 * taker_imbalance_score
                + 0.20 * c.wallet_cohort_score
                + 0.10 * c.smart_wallet_coord_score
                + 0.18 * dip_recovery_score
                + 0.08 * c.accumulation_conviction
                + 0.06 * liquidity_safety_score
                + 0.03 * freshness_bonus
                - 0.05 * concentration_penalty
                - exec_cost_penalty
            ) * quality_multiplier
            threshold = self.DIP_THRESHOLD
        else:
            total = 0.0
            threshold = 999.0

        total = round(total, 6)
        return ScoreBreakdownV2(
            regime=regime,
            total_score=total,
            threshold=threshold,
            entry_allowed=bool(total > threshold),
            micro_vol_accel_z=round(micro_vol_accel_z, 6),
            taker_imbalance_score=round(taker_imbalance_score, 6),
            dip_recovery_score=round(dip_recovery_score, 6),
            liquidity_safety_score=round(liquidity_safety_score, 6),
            concentration_penalty=round(concentration_penalty, 6),
            oracle_divergence_score=round(oracle_divergence_score, 6),
            freshness_bonus=round(freshness_bonus, 6),
            exec_cost_penalty=round(exec_cost_penalty, 6),
            quality_multiplier=round(quality_multiplier, 6),
        )

    def _micro_vol_accel_z(self, c: CandidateSnapshot) -> float:
        baseline = c.mean_volume_5m_per_min_usd or max(c.mean_volume_1h_usd / 60.0, 1.0)
        std = c.std_volume_5m_per_min_usd or max(c.std_volume_1h_usd / 60.0, 1.0)
        z = (c.volume_1m_usd - baseline) / max(std, 1.0)
        return max(0.0, min(3.0, z))

    def _taker_imbalance_score(self, c: CandidateSnapshot) -> float:
        buy = max(0.0, c.taker_buy_volume_usd)
        sell = max(0.0, c.taker_sell_volume_usd)
        ratio = buy / max(sell, 1.0)
        if ratio <= 1.0:
            return 0.0
        return min(1.5, (ratio - 1.0) / 2.0)

    def _dip_recovery_score(self, c: CandidateSnapshot) -> float:
        if c.smart_wallet_netflow_during_dip_usd <= 0:
            return 0.0
        if not 0.10 <= c.price_drop_from_ath_pct <= 0.45:
            return 0.0
        drop_quality = 1.0 - abs(c.price_drop_from_ath_pct - 0.25) / 0.20
        flow_boost = min(1.0, c.smart_wallet_netflow_during_dip_usd / 5000.0)
        return max(0.0, min(1.0, 0.65 * drop_quality + 0.35 * flow_boost))

    def _liquidity_safety_score(self, c: CandidateSnapshot) -> float:
        liq_score = 1.0 if c.liquidity_usd >= 12000 else 0.5 if c.liquidity_usd >= 8000 else 0.0
        if c.jupiter_sell_impact_bps <= 35:
            sell_score = 1.0
        elif c.jupiter_sell_impact_bps <= 80:
            sell_score = max(0.0, 1.0 - ((c.jupiter_sell_impact_bps - 35.0) / 45.0))
        else:
            sell_score = 0.0
        base_amm_bonus = 1.0 if c.base_amm_liquidity_share >= 0.5 else 0.7 if c.base_amm_liquidity_share >= 0.3 else 0.4
        return round((0.50 * liq_score + 0.35 * sell_score + 0.15 * base_amm_bonus), 6)

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
        if age < 90:
            return 1.0
        if age < 180:
            return 0.6
        if age < 480:
            return 0.3
        return 0.0

    def _exec_cost_penalty(self, c: CandidateSnapshot, regime: str) -> float:
        buy_impact = max(0.0, c.jupiter_price_impact_bps)
        sell_impact = max(0.0, c.jupiter_sell_impact_bps)
        round_trip_fee = max(0.0, c.round_trip_fee_sol)
        penalty = 0.0
        if buy_impact > 35:
            penalty += min(2.0, (buy_impact - 35) / 110.0)
        if sell_impact > 45:
            penalty += min(2.0, (sell_impact - 45) / 90.0)
        if round_trip_fee > 0.0008:
            penalty += 0.15
        if c.jito_tip_hurdle_sol > 0.0015:
            penalty += 0.20
        if c.local_pool_p75_priority_fee_lamports > 15000:
            penalty += min(0.50, (c.local_pool_p75_priority_fee_lamports - 15000) / 100000.0)
        if c.estimated_priority_fee_lamports > 8000:
            penalty += 0.10
        if c.amm_reserve_drift_ratio > 0.01:
            penalty += min(0.75, c.amm_reserve_drift_ratio * 12.5)
        if regime == "SCALP" and c.jito_tip_hurdle_sol > 0.0010 and c.volume_15m_sustained_multiple < 2.0:
            penalty += 0.25
        return penalty

    def _quality_multiplier(self, c: CandidateSnapshot, regime: str) -> float:
        if c.volume_authenticity_ratio < 0.40:
            return 0.0
        if c.sybil_cluster_share_pct > 25.0:
            return 0.0
        if c.block_0_snipe_pct > 15.0:
            return 0.0
        if c.organic_taker_volume_ratio < 0.50:
            return 0.0
        multiplier = 1.0
        if not c.has_socials and c.pair_age_seconds > 300:
            multiplier *= 0.80
        if c.sol_15m_trend_bps < -50:
            multiplier *= 0.90
        if c.distance_from_smart_entry_pct > 0.40:
            multiplier *= 0.75
        if c.signed_buy_ratio < 1.0:
            multiplier *= max(0.0, c.signed_buy_ratio)
        if regime == "TREND" and c.base_amm_liquidity_share < 0.30:
            multiplier *= 0.70
        if c.route_uses_dynamic_liquidity_share > 0.80:
            multiplier *= 0.85
        return multiplier

    def _holder_growth_score(self, c: CandidateSnapshot) -> float:
        return max(0.0, min(1.0, c.holder_growth_24h_pct / 20.0))

    def _smart_entry_multiplier(self, c: CandidateSnapshot) -> float:
        if c.distance_from_smart_entry_pct <= 0.15:
            return 1.0
        if c.distance_from_smart_entry_pct <= 0.30:
            return 0.9
        if c.distance_from_smart_entry_pct <= 0.40:
            return 0.8
        return 0.65
