#!/usr/bin/env python3
"""supertrend_flip -- Supertrend direction flip with an ADX chop filter; the line trails.. Ported from sister-lab catalog (https://www.netpicks.com/supertrend-indicator/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "supertrend_flip", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "15m-4h", "indicators": "Supertrend(10,3), ADX(14)",
    "long": "Supertrend flips up (green) with ADX>20", "short": "Supertrend flips down (red) with ADX>20", "desc": "Supertrend direction flip with an ADX chop filter; the line trails.", "source": "sister-lab catalog: https://www.netpicks.com/supertrend-indicator/",
}


def signal(I, i, htf):
    d, d1, adx = I["st_dir"][i], I["st_dir"][i-1], I["adx"][i]
    if _nan(d, d1, adx):
        return None
    if d == 1 and d1 == -1 and adx > 20:        # ADX gate cuts chop whipsaws
        return "long"
    if d == -1 and d1 == 1 and adx > 20:
        return "short"
    return None
