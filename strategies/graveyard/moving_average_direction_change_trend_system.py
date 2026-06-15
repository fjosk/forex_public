#!/usr/bin/env python3
"""moving_average_direction_change_trend_system -- SMA20 slope vs a small filter band; trade direction changes with whipsaw suppression. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "moving_average_direction_change_trend_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma20, atr",
    "long": "SMA20 rises by more than 0.05 ATR over one bar (direction change up past filter)",
    "short": "SMA20 falls by more than 0.05 ATR over one bar (direction change down past filter)",
    "desc": "MA direction-change system: SMA slope exceeds a filter band to suppress whipsaws",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma Ch5 p.115",
}

FILTER_MULT = 0.05   # 5% of ATR as direction filter


def signal(ind, pos, htf=None):
    """Long when SMA slope > filter; short when SMA slope < -filter."""
    if pos < 1:
        return None
    sma = ind["sma20"][pos]
    sma1 = ind["sma20"][pos - 1]
    a = ind["atr"][pos]
    if nan(sma, sma1, a):
        return None
    delta = sma - sma1
    filt = FILTER_MULT * a
    if delta > filt:
        return "long"
    if delta < -filt:
        return "short"
    return None
