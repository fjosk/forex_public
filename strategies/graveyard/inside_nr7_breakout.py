#!/usr/bin/env python3
"""inside_nr7_breakout -- Volatility-contraction breakout.. Ported from sister-lab catalog (https://www.tradingview.com/scripts/nr7/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "inside_nr7_breakout", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'time_stop_h': 36, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "breakout", "tf": "15m-4h", "indicators": "Inside bar / NR7",
    "long": "Break above an inside-bar / NR7 high", "short": "Break below the low", "desc": "Volatility-contraction breakout.", "source": "sister-lab catalog: https://www.tradingview.com/scripts/nr7/",
}


def signal(I, i, htf):
    h, l, c = I["high"], I["low"], I["close"]
    if i < 8 or _nan(h[i], l[i], c[i], h[i-1], l[i-1]):
        return None
    inside = h[i-1] < h[i-2] and l[i-1] > l[i-2]
    rng = [h[k] - l[k] for k in range(i-7, i)]
    nr7 = (h[i-1] - l[i-1]) == min(rng) if all(x == x for x in rng) else False
    if inside or nr7:
        if c[i] > h[i-1]:
            return "long"
        if c[i] < l[i-1]:
            return "short"
    return None
