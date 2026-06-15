#!/usr/bin/env python3
"""hma_slope -- Hull MA slope flip (low-lag trend).. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/hull-moving-average).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "hma_slope", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "15m-4h", "indicators": "Hull MA(21)",
    "long": "HMA slope turns up", "short": "HMA slope turns down", "desc": "Hull MA slope flip (low-lag trend).", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/hull-moving-average",
}


def signal(I, i, htf):
    h, h1, h2 = I["hma21"][i], I["hma21"][i-1], I["hma21"][i-2]
    if _nan(h, h1, h2):
        return None
    if h > h1 and h1 <= h2:
        return "long"
    if h < h1 and h1 >= h2:
        return "short"
    return None
