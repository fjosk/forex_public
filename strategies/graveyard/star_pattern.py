#!/usr/bin/env python3
"""star_pattern -- Three-bar star reversal.. Ported from sister-lab catalog (https://www.investopedia.com/terms/m/morningstar.asp).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "star_pattern", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "pattern", "tf": "4h-1d", "indicators": "Morning/Evening star, EMA50",
    "long": "Morning star in a downtrend", "short": "Evening star in an uptrend", "desc": "Three-bar star reversal.", "source": "sister-lab catalog: https://www.investopedia.com/terms/m/morningstar.asp",
}


def signal(I, i, htf):
    o0, c0 = I["open"][i-2], I["close"][i-2]
    o1, c1 = I["open"][i-1], I["close"][i-1]
    o2, c2 = I["open"][i], I["close"][i]
    e50 = I["ema50"][i]
    if _nan(o0, c0, o1, c1, o2, c2, e50):
        return None
    b0 = abs(c0 - o0); b1 = abs(c1 - o1)
    mid0 = (o0 + c0) / 2.0
    morning = c0 < o0 and b1 < 0.5 * b0 and c2 > o2 and c2 > mid0 and c2 < e50
    evening = c0 > o0 and b1 < 0.5 * b0 and c2 < o2 and c2 < mid0 and c2 > e50
    if morning:
        return "long"
    if evening:
        return "short"
    return None
