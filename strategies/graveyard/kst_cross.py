#!/usr/bin/env python3
"""kst_cross -- Know Sure Thing momentum cross.. Ported from sister-lab catalog (https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/prings-know-sure-thing-kst).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "kst_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "4h-1d", "indicators": "KST + signal",
    "long": "KST crosses above signal", "short": "KST crosses below signal", "desc": "Know Sure Thing momentum cross.", "source": "sister-lab catalog: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/prings-know-sure-thing-kst",
}


def signal(I, i, htf):
    k, s, k1, s1 = I["kst"][i], I["kst_sig"][i], I["kst"][i-1], I["kst_sig"][i-1]
    if _nan(k, s, k1, s1):
        return None
    if _xup(k, k1, s, s1):
        return "long"
    if _xdn(k, k1, s, s1):
        return "short"
    return None
