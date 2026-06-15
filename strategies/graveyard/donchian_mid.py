#!/usr/bin/env python3
"""donchian_mid -- Donchian midline trend (Turtle channel).. Ported from sister-lab catalog (https://www.tradingview.com/support/solutions/43000502253-donchian-channels-dc/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "donchian_mid", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "1h-4h", "indicators": "Donchian(20) midline",
    "long": "Close crosses above midline with rising upper", "short": "Close crosses below midline with falling lower", "desc": "Donchian midline trend (Turtle channel).", "source": "sister-lab catalog: https://www.tradingview.com/support/solutions/43000502253-donchian-channels-dc/",
}


def signal(I, i, htf):
    c, c1, up, lo, up1, lo1 = (I["close"][i], I["close"][i-1], I["dc_up"][i], I["dc_lo"][i],
                               I["dc_up"][i-1], I["dc_lo"][i-1])
    if _nan(c, c1, up, lo, up1, lo1):
        return None
    mid = (up + lo) / 2.0; mid1 = (up1 + lo1) / 2.0
    if _xup(c, c1, mid, mid1) and up > up1:
        return "long"
    if _xdn(c, c1, mid, mid1) and lo < lo1:
        return "short"
    return None
