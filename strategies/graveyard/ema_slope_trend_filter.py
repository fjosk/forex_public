#!/usr/bin/env python3
"""ema_slope_trend_filter -- EMA20 slope direction gate: long-only when EMA rising, short-only when falling. Elder Come Into My Trading Room Ch.5.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema_slope_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema20",
    "long": "EMA20 slope turns from down to up (EMA20[i] > EMA20[i-1] and EMA20[i-1] <= EMA20[i-2])",
    "short": "EMA20 slope turns from up to down (EMA20[i] < EMA20[i-1] and EMA20[i-1] >= EMA20[i-2])",
    "desc": "EMA slope-flip entry: enter on the bar the EMA slope direction changes; exit when slope flips again",
    "source": "come_into_my_trading_room_alexander_elder Ch.5 Moving Averages Trading Signals",
}


def signal(ind, pos, htf=None):
    """Enter on EMA20 slope flip (slope direction change bar)."""
    if pos < 2:
        return None
    e = ind["ema20"][pos]
    e1 = ind["ema20"][pos - 1]
    e2 = ind["ema20"][pos - 2]
    if nan(e, e1, e2):
        return None
    # slope flips to up: EMA was flat/down last bar, now rising
    if e > e1 and e1 <= e2:
        return "long"
    # slope flips to down
    if e < e1 and e1 >= e2:
        return "short"
    return None
