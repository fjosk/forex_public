#!/usr/bin/env python3
"""ad_oscillator_drf_zone -- Waters/Williams Accumulation-Distribution oscillator (gap-adjusted DRF, EMA(3)) reverses out of its 0.30/0.70 zones. Ported from sister-lab catalog (book:oscillator).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ad_oscillator_drf_zone", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "oscillator", "tf": "1h-4h", "indicators": "drf",
    "long": "Waters/Williams A/D (DRF) oscillator crosses up out of the oversold 0.30 zone", "short": "Waters/Williams A/D (DRF) oscillator crosses down out of the overbought 0.70 zone", "desc": "Waters/Williams Accumulation-Distribution oscillator (gap-adjusted DRF, EMA(3)) reverses out of its 0.30/0.70 zones", "source": "sister-lab catalog: book:oscillator",
}


def signal(I, i, htf):
    if i < 1:
        return None
    d = I["drf"][i]
    d1 = I["drf"][i-1]
    if _nan(d, d1):
        return None
    if d1 <= 0.30 and d > 0.30:
        return "long"
    if d1 >= 0.70 and d < 0.70:
        return "short"
    return None
