from dataclasses import dataclass, field


DEFAULT_ATA_RENT_EXEMPT_SOL = 0.00203928
DEFAULT_BASE_TX_FEE_SOL = 0.000005


@dataclass(slots=True)
class FillSimulation:
    expected_fill_rate: float
    extra_slippage_bps: float
    failed_fill_probability: float
    fee_drag_sol: float
    status_bias: str
    network_cost_breakdown_sol: dict[str, float] = field(default_factory=dict)


class BootstrapMEVSimulator:
    """
    Lightweight bootstrap simulator for replay realism.

    It intentionally biases fills against the trader in the exact cases that
    tend to look best in naive backtests: strong upward next-bar moves on small
    capital, stale aggregator quotes, and expensive local fee contention.
    """

    def simulate(
        self,
        *,
        vol_accel_z: float,
        sell_impact_bps: float,
        next_return_pct: float | None = None,
        jito_tip_hurdle_sol: float = 0.0,
        local_pool_priority_fee_lamports: int = 0,
        amm_reserve_drift_ratio: float = 0.0,
        base_tx_fee_sol: float = DEFAULT_BASE_TX_FEE_SOL,
        is_entry: bool = False,
        is_full_exit: bool = False,
        ata_exists: bool = True,
        ata_rent_exempt_sol: float = DEFAULT_ATA_RENT_EXEMPT_SOL,
        reclaim_ata_rent_on_full_exit: bool = False,
    ) -> FillSimulation:
        extra_slippage_bps = 0.0
        failed_fill_probability = 0.0
        status_bias = "NEUTRAL"

        if vol_accel_z > 2.5:
            failed_fill_probability += 0.35
            extra_slippage_bps += 60.0
            status_bias = "MEV_CONTESTED"
        if sell_impact_bps > 80:
            failed_fill_probability += 0.25
            extra_slippage_bps += 40.0
            status_bias = "EXIT_HOSTILE"
        if amm_reserve_drift_ratio > 0.02:
            failed_fill_probability += 0.20
            extra_slippage_bps += 25.0
            status_bias = "CACHE_LAG_RISK"
        if local_pool_priority_fee_lamports > 15000:
            failed_fill_probability += min(0.25, (local_pool_priority_fee_lamports - 15000) / 100000.0)
        if next_return_pct is not None:
            if next_return_pct >= 0.15:
                failed_fill_probability += 0.45
                extra_slippage_bps += 50.0
                status_bias = "ADVERSE_SELECTION_UP"
            elif next_return_pct <= -0.10:
                failed_fill_probability = max(0.0, failed_fill_probability - 0.20)
                status_bias = "ADVERSE_SELECTION_DOWN"

        failed_fill_probability = min(1.0, max(0.0, failed_fill_probability))
        expected_fill_rate = max(0.0, 1.0 - failed_fill_probability)

        failed_tx_fee_drag_sol = failed_fill_probability * max(0.0, base_tx_fee_sol)
        ata_rent_fee_sol = max(0.0, ata_rent_exempt_sol) if (is_entry and not ata_exists) else 0.0
        rent_reclaim_sol = (
            max(0.0, ata_rent_exempt_sol)
            if (is_full_exit and ata_exists and reclaim_ata_rent_on_full_exit)
            else 0.0
        )

        network_base_fee_sol = max(0.0, base_tx_fee_sol)
        mev_tip_fee_sol = max(0.0, jito_tip_hurdle_sol)

        fee_drag_sol = network_base_fee_sol + mev_tip_fee_sol + failed_tx_fee_drag_sol + ata_rent_fee_sol - rent_reclaim_sol
        fee_drag_sol = max(0.0, fee_drag_sol)

        breakdown = {
            "network_base_fee_sol": round(network_base_fee_sol, 8),
            "mev_tip_fee_sol": round(mev_tip_fee_sol, 8),
            "failed_tx_fee_drag_sol": round(failed_tx_fee_drag_sol, 8),
            "ata_rent_fee_sol": round(ata_rent_fee_sol, 8),
            "rent_reclaim_sol": round(rent_reclaim_sol, 8),
            "net_fee_drag_sol": round(fee_drag_sol, 8),
        }

        return FillSimulation(
            expected_fill_rate=round(expected_fill_rate, 4),
            extra_slippage_bps=round(extra_slippage_bps, 4),
            failed_fill_probability=round(failed_fill_probability, 4),
            fee_drag_sol=round(fee_drag_sol, 8),
            status_bias=status_bias,
            network_cost_breakdown_sol=breakdown,
        )
