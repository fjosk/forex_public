#!/usr/bin/env python3
"""aroon_cross -- Aroon up/down cross with strength gate.. Ported from sister-lab catalog (https://gocharting.com/docs/charting/technical-indicator/momentum/aroon-indicator).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "aroon_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "1h-1d", "indicators": "Aroon(25)",
    "long": "AroonUp crosses above AroonDown and AroonUp>=70", "short": "AroonDown crosses above AroonUp and >=70", "desc": "Aroon up/down cross with strength gate.", "source": "sister-lab catalog: https://gocharting.com/docs/charting/technical-indicator/momentum/aroon-indicator",
}


def signal(I, i, htf):
    au, ad, au1, ad1 = I["aroon_up"][i], I["aroon_dn"][i], I["aroon_up"][i-1], I["aroon_dn"][i-1]
    if _nan(au, ad, au1, ad1):
        return None
    if _xup(au, au1, ad, ad1) and au >= 70:
        return "long"
    if _xup(ad, ad1, au, au1) and ad >= 70:
        return "short"
    return None
