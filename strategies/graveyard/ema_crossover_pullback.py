#!/usr/bin/env python3
"""ema_crossover_pullback -- EMA Crossover with Pullback Confirmation (zeta-zetra).
web:https://github.com/zeta-zetra/code
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "ema_crossover_pullback",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h",
    "indicators": "ema9, ema50, high, low, close",
    "long": "ema9 (proxy 10) crosses above ema50 (proxy 40) AND wider range 2 bars ago AND close > high[-2]",
    "short": "ema9 crosses below ema50 AND wider range 2 bars ago AND close < low[-2]",
    "desc": "EMA crossover + volatility expansion breakout: fresh cross only valid if price breaks wider bar",
    "source": "web:https://github.com/zeta-zetra/code",
}


def signal(ind, pos, htf=None):
    """EMA10/40 crossover (approx ema9/ema50) with range-expansion breakout filter."""
    if pos < 2:
        return None
    e9 = ind["ema9"][pos]
    e50 = ind["ema50"][pos]
    e9_1 = ind["ema9"][pos - 1]
    e50_1 = ind["ema50"][pos - 1]
    c = ind["close"][pos]
    h2 = ind["high"][pos - 2]
    h1 = ind["high"][pos - 1]
    lo2 = ind["low"][pos - 2]
    lo1 = ind["low"][pos - 1]
    if nan(e9, e50, e9_1, e50_1, c, h2, h1, lo2, lo1):
        return None
    range_wide = h2 > h1 and lo2 < lo1
    if not range_wide:
        return None
    if _xup(e9, e9_1, e50, e50_1) and c > h2:
        return "long"
    if _xdn(e9, e9_1, e50, e50_1) and c < lo2:
        return "short"
    return None
