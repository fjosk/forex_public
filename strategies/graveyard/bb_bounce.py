#!/usr/bin/env python3
"""bb_bounce -- Bollinger band bounce: require close back inside, not a raw touch.. Ported from sister-lab catalog (https://www.fmz.com/lang/en/strategy/500992).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "bb_bounce", "cadences": ['day', 'scalp'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "15m-1h", "indicators": "Bollinger(20,2)",
    "long": "Prior bar pierced lower band, this bar closes back inside", "short": "Prior bar pierced upper band, this bar closes back inside", "desc": "Bollinger band bounce: require close back inside, not a raw touch.", "source": "sister-lab catalog: https://www.fmz.com/lang/en/strategy/500992",
}


def signal(I, i, htf):
    lo, lo1, up, up1 = I["bb_lo"][i], I["bb_lo"][i-1], I["bb_up"][i], I["bb_up"][i-1]
    c, c1, l1, h1 = I["close"][i], I["close"][i-1], I["low"][i-1], I["high"][i-1]
    if _nan(lo, lo1, up, up1, c, c1, l1, h1):
        return None
    if l1 < lo1 and c > lo:          # prior bar pierced lower band, this bar closes back inside
        return "long"
    if h1 > up1 and c < up:
        return "short"
    return None
