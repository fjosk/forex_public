#!/usr/bin/env python3
"""daily_pivot_bounce -- Classic floor-pivot bounce, 00:00-UTC anchor.. Ported from sister-lab catalog (https://www.babypips.com/learn/forex/other-pivot-point-calculation-methods).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "daily_pivot_bounce", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "1h (UTC-day)", "indicators": "Classic pivots S1/R1",
    "long": "Tag S1 and close back above with bullish bar", "short": "Tag R1 and close back below with bearish bar", "desc": "Classic floor-pivot bounce, 00:00-UTC anchor.", "source": "sister-lab catalog: https://www.babypips.com/learn/forex/other-pivot-point-calculation-methods",
}


def signal(I, i, htf):
    lo, hi, c, o = I["low"][i], I["high"][i], I["close"][i], I["open"][i]
    s1, r1 = I["piv_s1"][i], I["piv_r1"][i]
    if _nan(s1, r1, lo, hi, c, o):
        return None
    if lo <= s1 and c > s1 and c > o:        # tag support, close back above, bullish
        return "long"
    if hi >= r1 and c < r1 and c < o:
        return "short"
    return None
