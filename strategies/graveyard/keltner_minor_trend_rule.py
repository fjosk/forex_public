#!/usr/bin/env python3
"""keltner_minor_trend_rule -- Minor trend turns up on new bar high, down on new bar low; always-in. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "keltner_minor_trend_rule",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "high, low",
    "long": "price trades above the most recent bar high (new 1-bar high breakout); always reverse",
    "short": "price trades below the most recent bar low (new 1-bar low breakout); always reverse",
    "desc": "Keltner Minor Trend Rule: always-in stop-and-reverse on 1-bar new high/low",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """1-bar new high = long, 1-bar new low = short; stop-and-reverse."""
    if pos < 2:
        return None
    h = ind["high"]
    l = ind["low"]
    if nan(h[pos], l[pos], h[pos - 1], l[pos - 1]):
        return None
    if h[pos] > h[pos - 1]:
        return "long"
    if l[pos] < l[pos - 1]:
        return "short"
    return None
