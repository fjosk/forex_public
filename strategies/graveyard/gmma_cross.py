#!/usr/bin/env python3
"""gmma_cross -- Guppy Multiple Moving Average dual-ribbon crossover.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/moving-average-trading-strategies/guppy-multiple-moving-average-an-ma-ribbon-).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "gmma_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "1h-4h", "indicators": "GMMA dual EMA ribbons {3..15}/{30..60}",
    "long": "Short ribbon mean crosses above long ribbon mean", "short": "Short ribbon mean crosses below long ribbon mean", "desc": "Guppy Multiple Moving Average dual-ribbon crossover.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/moving-average-trading-strategies/guppy-multiple-moving-average-an-ma-ribbon-",
}


def signal(I, i, htf):
    s, l, s1, l1 = I["gmma_s"][i], I["gmma_l"][i], I["gmma_s"][i-1], I["gmma_l"][i-1]
    if _nan(s, l, s1, l1):
        return None
    if _xup(s, s1, l, l1):
        return "long"
    if _xdn(s, s1, l, l1):
        return "short"
    return None
