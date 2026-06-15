#!/usr/bin/env python3
"""cup_and_cap_3bar_countertrend -- 3-bar cup/cap countertrend setup: middle bar is extreme in trend direction. trading_systems_and_methods_kaufman_perry_j_kaufma.

In an uptrend, a CUP (middle bar has the lowest close of 3) signals exhaustion; sell when close breaks below middle bar low.
In a downtrend, a CAP (middle bar has the highest high of 3) signals exhaustion; buy when close breaks above middle bar high.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "cup_and_cap_3bar_countertrend",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "4h",
    "indicators": "close,high,low,open,sma20",
    "long": "CAP pattern (downtrend): middle of 3 bars has highest high; current close breaks above that high",
    "short": "CUP pattern (uptrend): middle of 3 bars has lowest close; current close breaks below middle bar low",
    "desc": "3-bar cup/cap countertrend: exhaustion at the highest/lowest middle bar in the trend direction",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma, Ch9 Cups and Caps p.227",
}


def signal(ind, pos, htf=None):
    """Cup (sell) and cap (buy) 3-bar countertrend pattern."""
    if pos < 3:
        return None
    c = ind["close"][pos]
    # Middle bar index: pos - 1; neighbors: pos-2 and pos (current acts as right bar trigger)
    c1 = ind["close"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c2 = ind["close"][pos - 2]
    h2 = ind["high"][pos - 2]
    l2 = ind["low"][pos - 2]
    c3 = ind["close"][pos - 3]
    sma = ind["sma20"][pos]
    if nan(c, c1, h1, l1, c2, h2, l2, c3, sma):
        return None
    # Trend context: sma20 slope
    sma_old = ind["sma20"][pos - 3]
    if nan(sma_old):
        return None
    uptrend = sma > sma_old
    downtrend = sma < sma_old
    # CUP in uptrend: middle bar (pos-1) has the lowest close among 3 bars; sell below its low
    cup = c2 > c1 and c > c1  # middle close is lowest of 3
    if uptrend and cup and c < l1:
        return "short"
    # CAP in downtrend: middle bar has the highest high among 3 bars; buy above its high
    cap = h2 < h1 and ind["high"][pos] < h1  # middle high is highest of 3
    if downtrend and cap and c > h1:
        return "long"
    return None
