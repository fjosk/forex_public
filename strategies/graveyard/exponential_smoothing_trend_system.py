#!/usr/bin/env python3
"""exponential_smoothing_trend_system -- EMA slope vs ATR-scaled band filter; enter when EMA slope exceeds the filter threshold. Kaufman TSM Ch.5.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "exponential_smoothing_trend_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema20,atr",
    "long": "EMA20[i] - EMA20[i-1] > filter (ATR-scaled threshold, default 0.10 ATR)",
    "short": "EMA20[i] - EMA20[i-1] < -filter",
    "desc": "Kaufman exponential smoothing trend system: EMA slope must exceed an ATR-scaled filter to avoid whipsaw",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.5 Exponential Smoothing",
}

_FILTER_MULT = 0.10  # filter = 0.10 * ATR; spec uses E3 direction-change threshold


def signal(ind, pos, htf=None):
    """EMA slope vs ATR-scaled band."""
    if pos < 1:
        return None
    e = ind["ema20"][pos]
    e1 = ind["ema20"][pos - 1]
    atr = ind["atr"][pos]
    if nan(e, e1, atr):
        return None
    filt = _FILTER_MULT * atr
    slope = e - e1
    if slope > filt:
        return "long"
    if slope < -filt:
        return "short"
    return None
