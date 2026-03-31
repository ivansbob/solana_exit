from src.strategy.exit_manager import DynamicExitManager, PositionState
from src.strategy.types import CandidateSnapshot


def make_candidate(**overrides):
    candidate = CandidateSnapshot(
        token_address="So11111111111111111111111111111111111111112",
        symbol="EXIT",
        jupiter_sell_impact_bps=35,
        round_trip_fee_sol=0.0005,
        estimated_exit_fee_sol=0.0002,
        route_uses_dynamic_liquidity_share=0.0,
        distance_from_smart_entry_pct=0.0,
        smart_money_reference_pnl_pct=0.0,
        volume_decay_z=0.0,
    )
    for key, value in overrides.items():
        setattr(candidate, key, value)
    return candidate


def test_gross_green_but_net_negative_does_not_take_profit():
    position = PositionState(
        regime="SCALP",
        age_seconds=80,
        unrealized_pnl_pct=0.20,
        position_notional_sol=0.02,
        expected_exit_fee_sol=0.0006,
    )
    current = make_candidate(jupiter_sell_impact_bps=90, volume_decay_z=-2.0)

    decision = DynamicExitManager().evaluate(position, current)

    assert decision.should_exit is False
    assert decision.reason == "hold_scalp"


def test_hard_stop_loss_triggers_immediately():
    position = PositionState(
        regime="TREND",
        age_seconds=30,
        unrealized_pnl_pct=-0.13,
    )

    decision = DynamicExitManager().evaluate(position, make_candidate())

    assert decision.should_exit is True
    assert decision.reason == "hard_stop_loss"


def test_dynamic_liquidity_haircut_reduces_executable_pnl():
    manager = DynamicExitManager()
    position = PositionState(regime="DIP", age_seconds=10, unrealized_pnl_pct=0.08, position_notional_sol=1.0)

    without_dynamic = manager.net_executable_pnl_pct(position, make_candidate(route_uses_dynamic_liquidity_share=0.0))
    with_dynamic = manager.net_executable_pnl_pct(position, make_candidate(route_uses_dynamic_liquidity_share=1.0))

    assert with_dynamic < without_dynamic


def test_bagholder_penalty_makes_exit_more_defensive():
    manager = DynamicExitManager()
    position = PositionState(regime="DIP", age_seconds=10, unrealized_pnl_pct=0.08, position_notional_sol=1.0)

    healthy = manager.net_executable_pnl_pct(position, make_candidate(distance_from_smart_entry_pct=-0.05))
    underwater = manager.net_executable_pnl_pct(position, make_candidate(distance_from_smart_entry_pct=-0.40))

    assert underwater < healthy


def test_regime_aware_time_stops_still_work():
    manager = DynamicExitManager()

    scalp = manager.evaluate(
        PositionState(regime="SCALP", age_seconds=220, unrealized_pnl_pct=0.002),
        make_candidate(jupiter_sell_impact_bps=5, round_trip_fee_sol=0.0, estimated_exit_fee_sol=0.0),
    )
    dip = manager.evaluate(
        PositionState(regime="DIP", age_seconds=700, unrealized_pnl_pct=0.001),
        make_candidate(jupiter_sell_impact_bps=5, round_trip_fee_sol=0.0, estimated_exit_fee_sol=0.0),
    )
    trend = manager.evaluate(
        PositionState(regime="TREND", age_seconds=1900, unrealized_pnl_pct=-0.001),
        make_candidate(jupiter_sell_impact_bps=5, round_trip_fee_sol=0.0, estimated_exit_fee_sol=0.0),
    )

    assert scalp.should_exit is True and scalp.reason == "time_stop_no_follow_through"
    assert dip.should_exit is True and dip.reason == "dip_recovery_failed"
    assert trend.should_exit is True and trend.reason == "trend_time_stop"
