#!/usr/bin/env python3
"""hurst_gated_trend_following -- EMA20/50 cross permitted only when Hurst > 0.55 (trending regime). PyQuantLab."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "hurst_gated_trend_following",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "hurst, ema20, ema50",
    "long": "EMA20 crosses above EMA50 AND hurst > 0.55 (trending regime confirmed)",
    "short": "EMA20 crosses below EMA50 AND hurst > 0.55",
    "desc": "Hurst-gated EMA trend following: EMA20/50 cross only in trending regime (H > 0.55)",
    "source": "PyQuantLab Hurst regime filter (pyquantlab.medium.com); Macrosynergy FX Hurst application",
}

_HURST_TREND = 0.55


def signal(ind, pos, htf=None):
    """EMA crossover gated by Hurst exponent confirming a trending regime."""
    h = ind["hurst"][pos]
    e20 = ind["ema20"][pos]
    e20_1 = ind["ema20"][pos - 1]
    e50 = ind["ema50"][pos]
    e50_1 = ind["ema50"][pos - 1]
    if nan(h, e20, e20_1, e50, e50_1):
        return None
    if h <= _HURST_TREND:
        return None
    if _xup(e20, e20_1, e50, e50_1):
        return "long"
    if _xdn(e20, e20_1, e50, e50_1):
        return "short"
    return None
