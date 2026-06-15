#!/usr/bin/env python3
"""daily_fozzy_method -- Daily Fozzy Method: EMA13 direction + RSI above/below 50 + rising. ForexFactory.

Close above EMA13 with RSI > 50 and rising = long trend. Mirror for short.
EMA13 is used as the proxy for the original SMA13; RSI(14) proxies RSI(10) per spec note.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "daily_fozzy_method",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "ema13 (proxy for sma13), rsi (14, proxy for rsi10)",
    "long": "close > EMA13 and RSI > 50 and RSI rising",
    "short": "close < EMA13 and RSI < 50 and RSI falling",
    "desc": "Daily Fozzy Method: MA direction + RSI 50-level filter (ForexFactory 2007)",
    "source": "web:https://www.forexfactory.com/thread/7984-the-daily-fozzy-method",
}


def signal(ind, pos, htf=None):
    """EMA13 + RSI direction confirmation."""
    e13 = ind["ema13"][pos]
    rsi_v = ind["rsi"][pos]
    rsi1 = ind["rsi"][pos - 1]
    c = ind["close"][pos]
    if nan(e13, rsi_v, rsi1, c):
        return None
    if c > e13 and rsi_v > 50 and rsi_v > rsi1:
        return "long"
    if c < e13 and rsi_v < 50 and rsi_v < rsi1:
        return "short"
    return None
