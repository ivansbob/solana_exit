from dataclasses import dataclass

from src.strategy.types import CandidateSnapshot


@dataclass(slots=True)
class GateDecision:
    allowed: bool
    reason: str


class TinyCapitalRiskGates:
    def __init__(
        self,
        *,
        min_liquidity_usd: float = 8000.0,
        max_price_impact_bps: float = 40.0,
        max_sell_impact_bps: float = 80.0,
        max_sell_buy_impact_ratio: float = 1.5,
        max_total_fee_sol: float = 0.0005,
        max_round_trip_fee_sol: float = 0.0010,
        max_jito_tip_hurdle_sol: float = 0.0020,
        max_priority_fee_lamports: int = 8000,
        max_local_pool_priority_fee_lamports: int = 50000,
        max_eoa_wallet_concentration: float = 0.35,
        max_freshness_age_seconds: int = 180,
        max_rugcheck_risk_score: int = 5000,
        max_sybil_cluster_share_pct: float = 25.0,
        min_pool_age_seconds_for_breakout: int = 300,
        zombie_min_pool_age_seconds: int = 86400,
        zombie_max_baseline_volume_1m_usd: float = 25.0,
        max_block_0_snipe_pct: float = 15.0,
        min_lp_burn_ratio_pct: float = 99.0,
        min_signed_buy_ratio: float = 0.95,
        max_amm_reserve_drift_ratio: float = 0.02,
        min_base_amm_liquidity_share_for_trend: float = 0.30,
    ) -> None:
        self.min_liquidity_usd = min_liquidity_usd
        self.max_price_impact_bps = max_price_impact_bps
        self.max_sell_impact_bps = max_sell_impact_bps
        self.max_sell_buy_impact_ratio = max_sell_buy_impact_ratio
        self.max_total_fee_sol = max_total_fee_sol
        self.max_round_trip_fee_sol = max_round_trip_fee_sol
        self.max_jito_tip_hurdle_sol = max_jito_tip_hurdle_sol
        self.max_priority_fee_lamports = max_priority_fee_lamports
        self.max_local_pool_priority_fee_lamports = max_local_pool_priority_fee_lamports
        self.max_eoa_wallet_concentration = max_eoa_wallet_concentration
        self.max_freshness_age_seconds = max_freshness_age_seconds
        self.max_rugcheck_risk_score = max_rugcheck_risk_score
        self.max_sybil_cluster_share_pct = max_sybil_cluster_share_pct
        self.min_pool_age_seconds_for_breakout = min_pool_age_seconds_for_breakout
        self.zombie_min_pool_age_seconds = zombie_min_pool_age_seconds
        self.zombie_max_baseline_volume_1m_usd = zombie_max_baseline_volume_1m_usd
        self.max_block_0_snipe_pct = max_block_0_snipe_pct
        self.min_lp_burn_ratio_pct = min_lp_burn_ratio_pct
        self.min_signed_buy_ratio = min_signed_buy_ratio
        self.max_amm_reserve_drift_ratio = max_amm_reserve_drift_ratio
        self.min_base_amm_liquidity_share_for_trend = min_base_amm_liquidity_share_for_trend

    def evaluate(self, c: CandidateSnapshot, regime: str | None = None) -> GateDecision:
        regime = (regime or "").upper() or None

        if c.liquidity_usd < self.min_liquidity_usd:
            return GateDecision(False, "liquidity_below_floor")
        if c.jupiter_price_impact_bps > self.max_price_impact_bps:
            return GateDecision(False, "price_impact_too_high")
        if c.jupiter_sell_impact_bps > self.max_sell_impact_bps:
            return GateDecision(False, "sell_impact_too_high")
        if c.jupiter_price_impact_bps > 0:
            ratio = c.jupiter_sell_impact_bps / max(c.jupiter_price_impact_bps, 1e-9)
            if ratio > self.max_sell_buy_impact_ratio:
                return GateDecision(False, "sell_buy_impact_asymmetry_too_high")
        if c.estimated_total_fee_sol > self.max_total_fee_sol:
            return GateDecision(False, "estimated_total_fee_too_high")
        if c.round_trip_fee_sol > self.max_round_trip_fee_sol:
            return GateDecision(False, "round_trip_fee_too_high")
        if c.jito_tip_hurdle_sol > self.max_jito_tip_hurdle_sol:
            return GateDecision(False, "jito_tip_hurdle_too_high")
        if c.estimated_priority_fee_lamports > self.max_priority_fee_lamports:
            return GateDecision(False, "priority_fee_too_high")
        if c.local_pool_p75_priority_fee_lamports > self.max_local_pool_priority_fee_lamports:
            return GateDecision(False, "local_pool_priority_fee_too_high")
        if self._eoa_concentration(c) > self.max_eoa_wallet_concentration:
            return GateDecision(False, "holder_concentration_too_high")
        if self._is_zombie_token(c):
            return GateDecision(False, "zombie_token_inactive_baseline")
        if c.freshness_age_seconds > self.max_freshness_age_seconds:
            return GateDecision(False, "stale_candidate")
        if c.amm_reserve_drift_ratio > self.max_amm_reserve_drift_ratio:
            return GateDecision(False, "amm_reserve_drift_too_high")
        if c.rugcheck_status.lower() in {"danger", "scam"}:
            return GateDecision(False, "rugcheck_failed_status")
        if c.rugcheck_risk_score > self.max_rugcheck_risk_score:
            return GateDecision(False, "rugcheck_failed_high_risk")
        if c.mint_authority_present:
            return GateDecision(False, "mint_authority_present")
        if c.freeze_authority_present:
            return GateDecision(False, "freeze_authority_present")
        if c.transfer_hook_present:
            return GateDecision(False, "token2022_transfer_hook_present")
        if c.token2022_transfer_fee_bps > 0:
            return GateDecision(False, "token2022_transfer_fee_present")
        if c.token2022_default_frozen:
            return GateDecision(False, "token2022_default_frozen")
        if c.sybil_cluster_share_pct > self.max_sybil_cluster_share_pct:
            return GateDecision(False, "sybil_cluster_share_too_high")
        if c.block_0_snipe_pct > self.max_block_0_snipe_pct:
            return GateDecision(False, "block_0_snipe_too_high")
        if c.lp_burn_ratio_pct < self.min_lp_burn_ratio_pct:
            return GateDecision(False, "lp_burn_ratio_too_low")
        if c.signed_buy_ratio < self.min_signed_buy_ratio and (c.wallet_cohort_score > 0.0 or c.smart_wallet_coord_score > 0.0):
            return GateDecision(False, "smart_money_not_signed_buy_verified")
        if c.pair_age_seconds and c.pair_age_seconds < self.min_pool_age_seconds_for_breakout and regime in {None, "SCALP"}:
            return GateDecision(False, "pool_too_young_for_breakout")
        if c.freshness_age_seconds > 300 and not c.has_socials:
            return GateDecision(False, "no_socials_detected")
        if regime == "TREND" and c.base_amm_liquidity_share < self.min_base_amm_liquidity_share_for_trend:
            return GateDecision(False, "base_amm_liquidity_share_too_low_for_trend")
        return GateDecision(True, "passed")

    def _eoa_concentration(self, c: CandidateSnapshot) -> float:
        if c.eoa_wallet_concentration > 0:
            return c.eoa_wallet_concentration
        return c.top_wallet_concentration

    def _is_zombie_token(self, c: CandidateSnapshot) -> bool:
        baseline_1m = c.mean_volume_5m_per_min_usd or (c.mean_volume_1h_usd / 60.0)
        return c.pair_age_seconds >= self.zombie_min_pool_age_seconds and baseline_1m <= self.zombie_max_baseline_volume_1m_usd
