#!/usr/bin/env python3
"""camarilla_reversal -- Camarilla L3/H3 reversion, 00:00-UTC anchor.. Ported from sister-lab catalog (https://www.babypips.com/learn/forex/other-pivot-point-calculation-methods).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "camarilla_reversal", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "1h (UTC-day)", "indicators": "Camarilla S3/R3",
    "long": "Tag S3 and close back above", "short": "Tag R3 and close back below", "desc": "Camarilla L3/H3 reversion, 00:00-UTC anchor.", "source": "sister-lab catalog: https://www.babypips.com/learn/forex/other-pivot-point-calculation-methods",
}


def signal(I, i, htf):
    lo, hi, c = I["low"][i], I["high"][i], I["close"][i]
    s3, r3 = I["cam_s3"][i], I["cam_r3"][i]
    if _nan(s3, r3, lo, hi, c):
        return None
    if lo <= s3 and c > s3:
        return "long"
    if hi >= r3 and c < r3:
        return "short"
    return None
