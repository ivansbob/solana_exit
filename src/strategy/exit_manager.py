from dataclasses import dataclass

from src.strategy.types import CandidateSnapshot


@dataclass(slots=True)
class PositionState:
    regime: str
    age_seconds: int
    unrealized_pnl_pct: float
    # Exit-time economics context used by executable PnL logic
    position_notional_sol: float = 1.0
    realized_fee_drag_sol: float = 0.0
    expected_exit_fee_sol: float = 0.0


@dataclass(slots=True)
class ExitDecision:
    should_exit: bool
    reason: str
    action: str = "HOLD"
    size_fraction: float = 0.0


@dataclass(slots=True)
class ExitThresholds:
    hard_stop_loss_pct: float = -0.12
    scalp_time_stop_age_seconds: int = 180
    scalp_time_stop_max_pnl_pct: float = 0.005
    scalp_take_profit_net_pct: float = 0.15
    scalp_trail_partial_net_pct: float = 0.25
    dip_time_stop_age_seconds: int = 600
    dip_time_stop_max_pnl_pct: float = 0.003
    dip_take_profit_net_pct: float = 0.18
    trend_time_stop_age_seconds: int = 1800
    trend_time_stop_max_pnl_pct: float = 0.0
    trend_take_profit_net_pct: float = 0.30
    dynamic_liquidity_haircut_multiplier: float = 0.35
    bagholder_underwater_distance_pct: float = -0.25
    bagholder_penalty_pct: float = 0.03


class DynamicExitManager:
    def __init__(self, thresholds: ExitThresholds | None = None):
        self.thresholds = thresholds or ExitThresholds()

    def net_executable_pnl_pct(self, position: PositionState, current: CandidateSnapshot) -> float:
        """Estimate executable PnL after impact, dynamic-liquidity haircut, and fee drag."""
        sell_impact_pct = current.jupiter_sell_impact_bps / 10000.0
        dynamic_liquidity_haircut_pct = (
            current.route_uses_dynamic_liquidity_share * sell_impact_pct * self.thresholds.dynamic_liquidity_haircut_multiplier
        )

        notional_sol = max(position.position_notional_sol, 1e-9)
        fee_drag_pct = (
            current.round_trip_fee_sol
            + current.estimated_exit_fee_sol
            + position.realized_fee_drag_sol
            + position.expected_exit_fee_sol
        ) / notional_sol

        net_pnl_pct = position.unrealized_pnl_pct - sell_impact_pct - dynamic_liquidity_haircut_pct - fee_drag_pct

        if (
            current.distance_from_smart_entry_pct <= self.thresholds.bagholder_underwater_distance_pct
            or current.smart_money_reference_pnl_pct <= self.thresholds.bagholder_underwater_distance_pct
        ):
            net_pnl_pct -= self.thresholds.bagholder_penalty_pct

        return net_pnl_pct

    def evaluate(self, position: PositionState, current: CandidateSnapshot) -> ExitDecision:
        thresholds = self.thresholds
        net_pnl_pct = self.net_executable_pnl_pct(position, current)

        if net_pnl_pct <= thresholds.hard_stop_loss_pct:
            return ExitDecision(True, "hard_stop_loss", "EXIT_ALL", 1.0)
        if current.smart_money_distribution_rate > 0.40:
            return ExitDecision(True, "smart_money_dumping", "EXIT_ALL", 1.0)
        if current.jupiter_sell_impact_bps > 100:
            return ExitDecision(True, "liquidity_withdrawn", "EXIT_ALL", 1.0)

        regime = position.regime.upper()
        if regime == "SCALP":
            if position.age_seconds >= thresholds.scalp_time_stop_age_seconds and net_pnl_pct <= thresholds.scalp_time_stop_max_pnl_pct:
                return ExitDecision(True, "time_stop_no_follow_through", "EXIT_ALL", 1.0)
            if net_pnl_pct >= thresholds.scalp_take_profit_net_pct and current.volume_decay_z < -1.5:
                return ExitDecision(True, "momentum_exhaustion_take_profit", "EXIT_ALL", 1.0)
            if net_pnl_pct >= thresholds.scalp_trail_partial_net_pct and current.volume_decay_z < -0.8:
                return ExitDecision(True, "trail_partial_scalp", "EXIT_PARTIAL", 0.5)
            return ExitDecision(False, "hold_scalp")

        if regime == "DIP":
            if position.age_seconds >= thresholds.dip_time_stop_age_seconds and net_pnl_pct <= thresholds.dip_time_stop_max_pnl_pct:
                return ExitDecision(True, "dip_recovery_failed", "EXIT_ALL", 1.0)
            if net_pnl_pct >= thresholds.dip_take_profit_net_pct and current.volume_decay_z < -1.2:
                return ExitDecision(True, "dip_take_profit", "EXIT_PARTIAL", 0.6)
            return ExitDecision(False, "hold_dip")

        if regime == "TREND":
            if position.age_seconds >= thresholds.trend_time_stop_age_seconds and net_pnl_pct <= thresholds.trend_time_stop_max_pnl_pct:
                return ExitDecision(True, "trend_time_stop", "EXIT_ALL", 1.0)
            if net_pnl_pct >= thresholds.trend_take_profit_net_pct and current.volume_decay_z < -1.0:
                return ExitDecision(True, "trend_partial_take_profit", "EXIT_PARTIAL", 0.5)
            return ExitDecision(False, "hold_trend")

        return ExitDecision(False, "unknown_regime_hold")
