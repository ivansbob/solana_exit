from dataclasses import dataclass

from src.strategy.types import CandidateSnapshot


@dataclass(slots=True)
class PositionState:
    regime: str
    age_seconds: int
    unrealized_pnl_pct: float


@dataclass(slots=True)
class ExitDecision:
    should_exit: bool
    reason: str
    action: str = "HOLD"
    size_fraction: float = 0.0


class DynamicExitManager:
    def evaluate(self, position: PositionState, current: CandidateSnapshot) -> ExitDecision:
        if current.smart_money_distribution_rate > 0.40:
            return ExitDecision(True, "smart_money_dumping", "EXIT_ALL", 1.0)
        if current.jupiter_sell_impact_bps > 100:
            return ExitDecision(True, "liquidity_withdrawn", "EXIT_ALL", 1.0)

        regime = position.regime.upper()
        if regime == "SCALP":
            if position.age_seconds >= 180 and position.unrealized_pnl_pct <= 0.005:
                return ExitDecision(True, "time_stop_no_follow_through", "EXIT_ALL", 1.0)
            if position.unrealized_pnl_pct >= 0.15 and current.volume_decay_z < -1.5:
                return ExitDecision(True, "momentum_exhaustion_take_profit", "EXIT_ALL", 1.0)
            if position.unrealized_pnl_pct >= 0.25 and current.volume_decay_z < -0.8:
                return ExitDecision(True, "trail_partial_scalp", "EXIT_PARTIAL", 0.5)
            return ExitDecision(False, "hold_scalp")

        if regime == "DIP":
            if position.age_seconds >= 600 and position.unrealized_pnl_pct <= 0.003:
                return ExitDecision(True, "dip_recovery_failed", "EXIT_ALL", 1.0)
            if position.unrealized_pnl_pct >= 0.18 and current.volume_decay_z < -1.2:
                return ExitDecision(True, "dip_take_profit", "EXIT_PARTIAL", 0.6)
            return ExitDecision(False, "hold_dip")

        if regime == "TREND":
            if position.age_seconds >= 1800 and position.unrealized_pnl_pct <= 0.0:
                return ExitDecision(True, "trend_time_stop", "EXIT_ALL", 1.0)
            if position.unrealized_pnl_pct >= 0.30 and current.volume_decay_z < -1.0:
                return ExitDecision(True, "trend_partial_take_profit", "EXIT_PARTIAL", 0.5)
            return ExitDecision(False, "hold_trend")

        return ExitDecision(False, "unknown_regime_hold")
