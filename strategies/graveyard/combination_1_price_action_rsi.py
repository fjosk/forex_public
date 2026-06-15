#!/usr/bin/env python3
"""combination_1_price_action_rsi -- Multi-bar OHLC + RSI14 + close_sma5 composite entry. zeta-zetra GitHub."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "combination_1_price_action_rsi",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "open, high, low, close, rsi, close_sma5",
    "long": "prev_open > curr_high AND curr_open > prev_close AND prev_low > curr_close AND RSI < 80 AND close > sma5",
    "short": "prev_open < curr_low AND curr_open < prev_close AND prev_high < curr_close AND RSI > 20 AND close < sma5",
    "desc": "Five-condition price action combination: multi-bar OHLC + RSI + SMA5 momentum filter",
    "source": "zeta-zetra/code GitHub (testing forex strategies/entry_exits/combination_1.py)",
}


def signal(ind, pos, htf=None):
    """Five-condition price action composite signal with RSI and SMA5 momentum gate."""
    o = ind["open"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    c = ind["close"][pos]
    o1 = ind["open"][pos - 1]
    h1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    r = ind["rsi"][pos]
    sma5 = ind["close_sma5"][pos]
    if nan(o, h, lo, c, o1, h1, lo1, c1, r, sma5):
        return None
    if o1 > h and o > c1 and lo1 > c and r < 80 and c > sma5:
        return "long"
    if o1 < lo and o < c1 and h1 < c and r > 20 and c < sma5:
        return "short"
    return None
