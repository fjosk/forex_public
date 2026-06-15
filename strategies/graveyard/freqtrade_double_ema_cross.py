#!/usr/bin/env python3
"""freqtrade_double_ema_cross -- EMA9/21 crossover filtered by EMA200 regime. paulcpk freqtrade."""
from strategies._common import nan, TREND_FLIP, _xup, ALL_CLASSES

META = {
    "id": "freqtrade_double_ema_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema9, ema21, ema200, low",
    "long": "ema9 crosses above ema21 AND candle low > ema200",
    "short": "not used (long-only per source); reverse cross triggers exit",
    "desc": "Double EMA crossover (9/21) with EMA200 trend regime filter",
    "source": "https://github.com/paulcpk/freqtrade-strategies-that-work/blob/master/DoubleEMACrossoverWithTrend.py",
}


def signal(ind, pos, htf=None):
    """EMA9 x EMA21 crossover filtered by EMA200."""
    e9 = ind["ema9"][pos]
    e9_1 = ind["ema9"][pos - 1]
    e21 = ind["ema21"][pos]
    e21_1 = ind["ema21"][pos - 1]
    e200 = ind["ema200"][pos]
    lo = ind["low"][pos]
    if nan(e9, e9_1, e21, e21_1, e200, lo):
        return None
    if _xup(e9, e9_1, e21, e21_1) and lo > e200:
        return "long"
    if _xup(e21, e21_1, e9, e9_1) or lo < e200:
        return "short"
    return None
