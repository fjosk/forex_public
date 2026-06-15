#!/usr/bin/env python3
"""three_soldiers -- Three-candle momentum thrust.. Ported from sister-lab catalog (https://www.investopedia.com/terms/t/three_white_soldiers.asp).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "three_soldiers", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "pattern", "tf": "1h-1d", "indicators": "Three soldiers/crows",
    "long": "Three white soldiers", "short": "Three black crows", "desc": "Three-candle momentum thrust.", "source": "sister-lab catalog: https://www.investopedia.com/terms/t/three_white_soldiers.asp",
}


def signal(I, i, htf):
    o0, c0 = I["open"][i-2], I["close"][i-2]
    o1, c1 = I["open"][i-1], I["close"][i-1]
    o2, c2 = I["open"][i], I["close"][i]
    if _nan(o0, c0, o1, c1, o2, c2):
        return None
    up = c0 > o0 and c1 > o1 and c2 > o2 and c2 > c1 > c0 and o1 > o0 and o1 < c0 and o2 > o1 and o2 < c1
    dn = c0 < o0 and c1 < o1 and c2 < o2 and c2 < c1 < c0 and o1 < o0 and o1 > c0 and o2 < o1 and o2 > c1
    if up:
        return "long"
    if dn:
        return "short"
    return None
