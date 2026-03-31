from src.ingest.jupiter_route_analyzer import JupiterRouteAnalyzer


def test_route_analyzer_estimates_base_and_dynamic_shares():
    quote = {
        "routePlan": [
            {"percent": 60, "swapInfo": {"label": "Raydium AMM"}},
            {"percent": 40, "swapInfo": {"label": "Meteora DLMM"}},
        ]
    }
    profile = JupiterRouteAnalyzer().analyze_quote(quote)
    assert profile.step_count == 2
    assert round(profile.base_amm_liquidity_share, 2) == 0.60
    assert round(profile.dynamic_liquidity_share, 2) == 0.40


def test_route_analyzer_handles_missing_weights():
    quote = {
        "routePlan": [
            {"swapInfo": {"label": "Orca Classic"}},
            {"swapInfo": {"label": "Whirlpool"}},
        ]
    }
    profile = JupiterRouteAnalyzer().analyze_quote(quote)
    assert profile.step_count == 2
    assert round(profile.base_amm_liquidity_share, 2) == 0.50
    assert round(profile.dynamic_liquidity_share, 2) == 0.50
