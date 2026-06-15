#!/usr/bin/env python3
"""ultimate_osc -- Ultimate Oscillator reversal out of extremes.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/ultimate-oscillator).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ultimate_osc", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "1h-4h", "indicators": "Ultimate Oscillator(7,14,28)",
    "long": "UO rises through 30", "short": "UO falls through 70", "desc": "Ultimate Oscillator reversal out of extremes.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/ultimate-oscillator",
}


def signal(I, i, htf):
    u, u1 = I["uo"][i], I["uo"][i-1]
    if _nan(u, u1):
        return None
    if u1 < 30 and u >= 30:
        return "long"
    if u1 > 70 and u <= 70:
        return "short"
    return None
