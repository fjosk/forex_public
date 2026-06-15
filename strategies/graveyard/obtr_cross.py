#!/usr/bin/env python3
"""obtr_cross -- On-Balance True Range (signed cumulative true range) crossing its 9-bar EMA signal line. Ported from sister-lab catalog (book:volume).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "obtr_cross", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "volume", "tf": "1h-4h", "indicators": "obtr,obtr_ema",
    "long": "On-Balance True Range oscillator crosses above its EMA(9) signal", "short": "On-Balance True Range oscillator crosses below its EMA(9) signal", "desc": "On-Balance True Range (signed cumulative true range) crossing its 9-bar EMA signal line", "source": "sister-lab catalog: book:volume",
}


def signal(I, i, htf):
    if i < 1:
        return None
    o = I["obtr"][i]
    sig = I["obtr_ema"][i]
    op = I["obtr"][i-1]
    sp = I["obtr_ema"][i-1]
    if _nan(o, sig, op, sp):
        return None
    if _xup(o, op, sig, sp):
        return "long"
    if _xdn(o, op, sig, sp):
        return "short"
    return None
