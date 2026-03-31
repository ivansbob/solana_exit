from src.paper.mev_simulator import BootstrapMEVSimulator


def test_failed_fills_produce_fee_drag():
    sim = BootstrapMEVSimulator().simulate(
        vol_accel_z=3.0,
        sell_impact_bps=95,
        next_return_pct=0.18,
        jito_tip_hurdle_sol=0.0,
        local_pool_priority_fee_lamports=30000,
        amm_reserve_drift_ratio=0.03,
    )

    assert sim.failed_fill_probability > 0.0
    assert sim.failed_attempt_fee_drag_sol > 0.0
    assert sim.fee_drag_sol >= sim.failed_attempt_fee_drag_sol


def test_replay_cost_breakdown_includes_failed_attempt_drag():
    sim = BootstrapMEVSimulator().simulate(
        vol_accel_z=0.0,
        sell_impact_bps=0.0,
        next_return_pct=None,
        jito_tip_hurdle_sol=0.0007,
        local_pool_priority_fee_lamports=15000,
        amm_reserve_drift_ratio=0.0,
    )

    assert sim.base_fee_drag_sol == 0.0007
    assert sim.failed_attempt_fee_drag_sol == 0.0
    assert sim.fee_drag_sol == sim.base_fee_drag_sol
