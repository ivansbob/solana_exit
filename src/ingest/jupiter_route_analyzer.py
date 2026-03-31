from __future__ import annotations

from dataclasses import dataclass
from typing import Any


BASE_AMM_LABEL_HINTS = (
    "raydium amm",
    "raydium cpmm",
    "orca v1",
    "orca classic",
)
DYNAMIC_LIQUIDITY_LABEL_HINTS = (
    "meteora",
    "dlmm",
    "whirlpool",
    "concentrated",
)


@dataclass(slots=True)
class RouteLiquidityProfile:
    base_amm_liquidity_share: float
    dynamic_liquidity_share: float
    step_count: int


class JupiterRouteAnalyzer:
    def analyze_quote(self, quote: dict[str, Any]) -> RouteLiquidityProfile:
        route_plan = quote.get("routePlan") or []
        if not route_plan:
            return RouteLiquidityProfile(0.0, 0.0, 0)

        total_weight = 0.0
        base_weight = 0.0
        dynamic_weight = 0.0
        for step in route_plan:
            weight = self._extract_weight(step)
            total_weight += weight
            label = self._extract_label(step)
            lower = label.lower()
            if any(h in lower for h in BASE_AMM_LABEL_HINTS):
                base_weight += weight
            if any(h in lower for h in DYNAMIC_LIQUIDITY_LABEL_HINTS):
                dynamic_weight += weight

        if total_weight <= 0:
            total_weight = float(len(route_plan))
            base_weight = float(sum(1 for step in route_plan if self._is_base(step)))
            dynamic_weight = float(sum(1 for step in route_plan if self._is_dynamic(step)))

        return RouteLiquidityProfile(
            base_amm_liquidity_share=round(base_weight / max(total_weight, 1e-9), 6),
            dynamic_liquidity_share=round(dynamic_weight / max(total_weight, 1e-9), 6),
            step_count=len(route_plan),
        )

    def _extract_weight(self, step: dict[str, Any]) -> float:
        for key in ("percent", "bps"):
            value = step.get(key)
            if value is None:
                continue
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
        return 1.0

    def _extract_label(self, step: dict[str, Any]) -> str:
        swap_info = step.get("swapInfo") or {}
        return str(swap_info.get("label") or step.get("label") or "")

    def _is_base(self, step: dict[str, Any]) -> bool:
        return any(h in self._extract_label(step).lower() for h in BASE_AMM_LABEL_HINTS)

    def _is_dynamic(self, step: dict[str, Any]) -> bool:
        return any(h in self._extract_label(step).lower() for h in DYNAMIC_LIQUIDITY_LABEL_HINTS)
