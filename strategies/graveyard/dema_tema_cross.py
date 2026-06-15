#!/usr/bin/env python3
"""dema_tema_cross -- Triple-EMA fast/slow cross (low lag).. Ported from sister-lab catalog (https://en.wikipedia.org/wiki/Double_exponential_moving_average).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "dema_tema_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "15m-1h", "indicators": "TEMA(9), TEMA(21)",
    "long": "TEMA9 crosses above TEMA21", "short": "TEMA9 crosses below TEMA21", "desc": "Triple-EMA fast/slow cross (low lag).", "source": "sister-lab catalog: https://en.wikipedia.org/wiki/Double_exponential_moving_average",
}


def signal(I, i, htf):
    f, s, f1, s1 = I["tema9"][i], I["tema21"][i], I["tema9"][i-1], I["tema21"][i-1]
    if _nan(f, s, f1, s1):
        return None
    if _xup(f, f1, s, s1):
        return "long"
    if _xdn(f, f1, s, s1):
        return "short"
    return None
