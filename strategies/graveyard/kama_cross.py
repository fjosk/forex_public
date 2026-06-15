#!/usr/bin/env python3
"""kama_cross -- Kaufman Adaptive MA cross with slope filter.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/kaufmans-adaptive-moving-average-kama).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "kama_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "1h-4h", "indicators": "KAMA(10,2,30)",
    "long": "Close crosses above rising KAMA", "short": "Close crosses below falling KAMA", "desc": "Kaufman Adaptive MA cross with slope filter.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/kaufmans-adaptive-moving-average-kama",
}


def signal(I, i, htf):
    c, c1, k, k1, k5 = I["close"][i], I["close"][i-1], I["kama"][i], I["kama"][i-1], I["kama"][i-5]
    if _nan(c, c1, k, k1, k5):
        return None
    if _xup(c, c1, k, k1) and k > k5:
        return "long"
    if _xdn(c, c1, k, k1) and k < k5:
        return "short"
    return None
