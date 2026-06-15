#!/usr/bin/env python3
"""classic_2day_swing_chart -- Classic chartist 2-day swing chart: two consecutive higher/lower bars confirm swing. trading_systems_and_methods_kaufman_perry_j_kaufma.

Swing change to up: two consecutive bars each with higher high AND higher low -> buy.
Swing change to down: two consecutive bars each with lower high AND lower low -> sell.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "classic_2day_swing_chart",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "high,low,close",
    "long": "bar[pos-1]: H>H[pos-2] AND L>L[pos-2]; bar[pos]: H>H[pos-1] AND L>L[pos-1] -> confirmed upswing",
    "short": "two consecutive bars each with lower H and lower L -> confirmed downswing",
    "desc": "2-day swing chart: two consecutive bars of higher-high-higher-low (or lower) confirm trend direction",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma, Ch12 pp.281-283",
}


def signal(ind, pos, htf=None):
    """Two consecutive higher-high+higher-low bars = upswing; two lower-high+lower-low = downswing."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    h2 = ind["high"][pos - 2]
    l2 = ind["low"][pos - 2]
    if nan(h, l, h1, l1, h2, l2):
        return None
    # Two consecutive bars with higher high AND higher low
    if h > h1 and l > l1 and h1 > h2 and l1 > l2:
        return "long"
    # Two consecutive bars with lower high AND lower low
    if h < h1 and l < l1 and h1 < h2 and l1 < l2:
        return "short"
    return None
