from src.paper.mev_simulator import BootstrapMEVSimulator


def test_first_entry_without_ata_charges_rent_drag():
    sim = BootstrapMEVSimulator().simulate(
        vol_accel_z=0.0,
        sell_impact_bps=10.0,
        is_entry=True,
        ata_exists=False,
        ata_rent_exempt_sol=0.00203928,
    )

    assert sim.network_cost_breakdown_sol["ata_rent_fee_sol"] == 0.00203928
    assert sim.fee_drag_sol >= 0.00203928


def test_full_exit_reclaims_rent_when_configured():
    sim = BootstrapMEVSimulator().simulate(
        vol_accel_z=0.0,
        sell_impact_bps=10.0,
        is_full_exit=True,
        ata_exists=True,
        reclaim_ata_rent_on_full_exit=True,
        ata_rent_exempt_sol=0.00203928,
    )

    assert sim.network_cost_breakdown_sol["rent_reclaim_sol"] == 0.00203928
    assert sim.fee_drag_sol < 0.001


def test_failed_attempts_add_nonzero_fee_drag():
    sim = BootstrapMEVSimulator().simulate(
        vol_accel_z=3.0,
        sell_impact_bps=120.0,
        next_return_pct=0.20,
        base_tx_fee_sol=0.000005,
    )

    assert sim.failed_fill_probability > 0.0
    assert sim.network_cost_breakdown_sol["failed_tx_fee_drag_sol"] > 0.0


def test_cost_breakdown_is_explicit_and_balanced():
    sim = BootstrapMEVSimulator().simulate(
        vol_accel_z=2.8,
        sell_impact_bps=30.0,
        next_return_pct=0.20,
        jito_tip_hurdle_sol=0.0012,
        is_entry=True,
        ata_exists=False,
    )

    breakdown = sim.network_cost_breakdown_sol
    assert set(breakdown) == {
        "network_base_fee_sol",
        "mev_tip_fee_sol",
        "failed_tx_fee_drag_sol",
        "ata_rent_fee_sol",
        "rent_reclaim_sol",
        "net_fee_drag_sol",
    }
    assert breakdown["net_fee_drag_sol"] == sim.fee_drag_sol
