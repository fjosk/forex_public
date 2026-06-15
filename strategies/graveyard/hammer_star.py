#!/usr/bin/env python3
"""hammer_star -- Hammer / shooting-star reversal.. Ported from sister-lab catalog (https://www.investopedia.com/terms/h/hammer.asp).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "hammer_star", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "pattern", "tf": "1h-4h", "indicators": "Hammer/Shooting-star, EMA50",
    "long": "Hammer (lower wick>=2x body) with close>EMA50", "short": "Shooting star with close<EMA50", "desc": "Hammer / shooting-star reversal.", "source": "sister-lab catalog: https://www.investopedia.com/terms/h/hammer.asp",
}


def signal(I, i, htf):
    o, h, l, c, e50 = I["open"][i], I["high"][i], I["low"][i], I["close"][i], I["ema50"][i]
    if _nan(o, h, l, c, e50):
        return None
    body = abs(c - o); lw = min(o, c) - l; uw = h - max(o, c)
    if body <= 0:
        return None
    if lw >= 2 * body and uw <= body and c > e50:
        return "long"
    if uw >= 2 * body and lw <= body and c < e50:
        return "short"
    return None
