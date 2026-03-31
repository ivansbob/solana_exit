from dataclasses import dataclass


@dataclass(slots=True)
class SimulationThresholds:
    contested_vol_accel_z: float = 2.5
    contested_fail_prob_add: float = 0.35
    contested_slippage_bps_add: float = 60.0
    hostile_sell_impact_bps: float = 80.0
    hostile_fail_prob_add: float = 0.25
    hostile_slippage_bps_add: float = 40.0
    reserve_drift_ratio_limit: float = 0.02
    reserve_drift_fail_prob_add: float = 0.20
    reserve_drift_slippage_bps_add: float = 25.0
    priority_fee_baseline_lamports: int = 15000
    priority_fee_fail_prob_cap: float = 0.25
    priority_fee_fail_prob_scale: float = 100000.0
    adverse_up_return_pct: float = 0.15
    adverse_up_fail_prob_add: float = 0.45
    adverse_up_slippage_bps_add: float = 50.0
    adverse_down_return_pct: float = -0.10
    adverse_down_fail_prob_relief: float = 0.20
    failed_attempt_flat_fee_sol: float = 0.000005


@dataclass(slots=True)
class FillSimulation:
    expected_fill_rate: float
    extra_slippage_bps: float
    failed_fill_probability: float
    failed_attempt_fee_drag_sol: float
    base_fee_drag_sol: float
    fee_drag_sol: float
    status_bias: str


class BootstrapMEVSimulator:
    """
    Lightweight bootstrap simulator for replay realism.

    It intentionally biases fills against the trader in the exact cases that
    tend to look best in naive backtests: strong upward next-bar moves on small
    capital, stale aggregator quotes, and expensive local fee contention.
    """

    def __init__(self, thresholds: SimulationThresholds | None = None):
        self.thresholds = thresholds or SimulationThresholds()

    def simulate(
        self,
        *,
        vol_accel_z: float,
        sell_impact_bps: float,
        next_return_pct: float | None = None,
        jito_tip_hurdle_sol: float = 0.0,
        local_pool_priority_fee_lamports: int = 0,
        amm_reserve_drift_ratio: float = 0.0,
    ) -> FillSimulation:
        t = self.thresholds
        extra_slippage_bps = 0.0
        failed_fill_probability = 0.0
        status_bias = "NEUTRAL"

        if vol_accel_z > t.contested_vol_accel_z:
            failed_fill_probability += t.contested_fail_prob_add
            extra_slippage_bps += t.contested_slippage_bps_add
            status_bias = "MEV_CONTESTED"
        if sell_impact_bps > t.hostile_sell_impact_bps:
            failed_fill_probability += t.hostile_fail_prob_add
            extra_slippage_bps += t.hostile_slippage_bps_add
            status_bias = "EXIT_HOSTILE"
        if amm_reserve_drift_ratio > t.reserve_drift_ratio_limit:
            failed_fill_probability += t.reserve_drift_fail_prob_add
            extra_slippage_bps += t.reserve_drift_slippage_bps_add
            status_bias = "CACHE_LAG_RISK"
        if local_pool_priority_fee_lamports > t.priority_fee_baseline_lamports:
            failed_fill_probability += min(
                t.priority_fee_fail_prob_cap,
                (local_pool_priority_fee_lamports - t.priority_fee_baseline_lamports) / t.priority_fee_fail_prob_scale,
            )
        if next_return_pct is not None:
            if next_return_pct >= t.adverse_up_return_pct:
                failed_fill_probability += t.adverse_up_fail_prob_add
                extra_slippage_bps += t.adverse_up_slippage_bps_add
                status_bias = "ADVERSE_SELECTION_UP"
            elif next_return_pct <= t.adverse_down_return_pct:
                failed_fill_probability = max(0.0, failed_fill_probability - t.adverse_down_fail_prob_relief)
                status_bias = "ADVERSE_SELECTION_DOWN"

        failed_fill_probability = min(1.0, failed_fill_probability)
        expected_fill_rate = max(0.0, 1.0 - failed_fill_probability)
        failed_attempt_fee_sol = max(0.0, t.failed_attempt_flat_fee_sol + (local_pool_priority_fee_lamports / 1_000_000_000))
        failed_attempt_fee_drag_sol = failed_fill_probability * failed_attempt_fee_sol
        base_fee_drag_sol = max(0.0, jito_tip_hurdle_sol)
        fee_drag_sol = base_fee_drag_sol + failed_attempt_fee_drag_sol
        return FillSimulation(
            expected_fill_rate=round(expected_fill_rate, 4),
            extra_slippage_bps=round(extra_slippage_bps, 4),
            failed_fill_probability=round(failed_fill_probability, 4),
            failed_attempt_fee_drag_sol=round(failed_attempt_fee_drag_sol, 8),
            base_fee_drag_sol=round(base_fee_drag_sol, 8),
            fee_drag_sol=round(fee_drag_sol, 8),
            status_bias=status_bias,
        )
