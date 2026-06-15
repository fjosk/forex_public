#!/usr/bin/env python3
"""hlhb_ema_rsi_adx -- HLHB EMA RSI ADX Trend Catcher (long only). freqtrade/babypips.

EMA5/EMA9 crossover with RSI crossing above 50 and ADX > 25. Long-only as sourced.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "hlhb_ema_rsi_adx",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5, ema9, rsi, adx",
    "long": "ema5 crosses above ema9 AND rsi crosses above 50 AND adx > 25",
    "short": "ema5 crosses below ema9 AND rsi crosses below 50 AND adx > 25",
    "desc": "HLHB EMA5/EMA9 crossover filtered by RSI mid-cross and ADX trend strength",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/hlhb.py",
}


def signal(ind, pos, htf=None):
    """HLHB EMA RSI ADX Trend Catcher."""
    e5, e9 = ind["ema5"][pos], ind["ema9"][pos]
    e51, e91 = ind["ema5"][pos - 1], ind["ema9"][pos - 1]
    r, r1 = ind["rsi"][pos], ind["rsi"][pos - 1]
    dx = ind["adx"][pos]
    if nan(e5, e9, e51, e91, r, r1, dx):
        return None
    if dx > 25 and _xup(e5, e51, e9, e91) and _xup(r, r1, 50.0, 50.0):
        return "long"
    if dx > 25 and _xdn(e5, e51, e9, e91) and _xdn(r, r1, 50.0, 50.0):
        return "short"
    return None
