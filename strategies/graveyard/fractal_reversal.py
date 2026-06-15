#!/usr/bin/env python3
"""fractal_reversal -- Bill Williams fractal reversal (2-bar confirmed).. Ported from sister-lab catalog (https://www.tradingview.com/scripts/williamsfractal/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "fractal_reversal", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "pattern", "tf": "1h-4h", "indicators": "Williams fractals, EMA50",
    "long": "Confirmed down-fractal with close>EMA50", "short": "Confirmed up-fractal with close<EMA50", "desc": "Bill Williams fractal reversal (2-bar confirmed).", "source": "sister-lab catalog: https://www.tradingview.com/scripts/williamsfractal/",
}


def signal(I, i, htf):
    fd, fu, c, e50 = I["frac_dn"][i], I["frac_up"][i], I["close"][i], I["ema50"][i]
    if _nan(c, e50):
        return None
    if fd and c > e50:           # confirmed down-fractal (swing low) in an uptrend
        return "long"
    if fu and c < e50:
        return "short"
    return None
