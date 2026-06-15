#!/usr/bin/env python3
"""single_ma_trend_price_vs_ma_penetration -- Hochheimer single-MA: close crosses EMA always-in. trading_systems_and_methods_kaufman_perry_j_kaufma.

Always-in stop-and-reverse: long when close > EMA50, short when close < EMA50.
Signal fires only on the bar when the cross occurs (entry bar).
Uses EMA50 as the representative period (Kaufman tests showed 40-70 bar optimal range).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "single_moving_average_trend_price_vs_ma_penetration",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,ema50",
    "long": "close closes above EMA50 (penetration from below)",
    "short": "close closes below EMA50 (penetration from above); always-in reverse",
    "desc": "Hochheimer single-MA penetration: stop-and-reverse on close crossing EMA50",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch21 Tables 21-2,21-3",
}


def signal(ind, pos, htf=None):
    """Single MA penetration: fire on the cross bar only."""
    if pos < 1:
        return None
    c  = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    e  = ind["ema50"][pos]
    e1 = ind["ema50"][pos - 1]
    if nan(c, c1, e, e1):
        return None
    if c > e and c1 <= e1:
        return "long"
    if c < e and c1 >= e1:
        return "short"
    return None
