#!/usr/bin/env python3
"""adx_di_cross -- Directional-index crossover gated by ADX>25 trend strength.. Ported from sister-lab catalog (https://www.avatrade.com/education/technical-analysis-indicators-strategies/adx-indicator-trading-strategies).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "adx_di_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "1h-4h", "indicators": "ADX(14), +DI(14), -DI(14)",
    "long": "+DI crosses above -DI AND ADX>25", "short": "-DI crosses above +DI AND ADX>25", "desc": "Directional-index crossover gated by ADX>25 trend strength.", "source": "sister-lab catalog: https://www.avatrade.com/education/technical-analysis-indicators-strategies/adx-indicator-trading-strategies",
}


def signal(I, i, htf):
    dp, dm, dp1, dm1, adx = I["di_plus"][i], I["di_minus"][i], I["di_plus"][i-1], I["di_minus"][i-1], I["adx"][i]
    if _nan(dp, dm, dp1, dm1, adx):
        return None
    if _xup(dp, dp1, dm, dm1) and adx > 25:
        return "long"
    if _xdn(dp, dp1, dm, dm1) and adx > 25:
        return "short"
    return None
