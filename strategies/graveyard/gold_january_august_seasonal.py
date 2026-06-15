#!/usr/bin/env python3
"""gold_january_august_seasonal -- Gold seasonal position: Jan and Aug strong windows.

XAU/USD historically strong in January, August, September, December.
Technical confirmation: close above ema50 AND rsi < 70 (not overbought).
Entry fires on the first bar of a strong month with technical alignment.
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "gold_january_august_seasonal",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "position",
    "tf": "daily",
    "indicators": "open_time, ema50, rsi, close",
    "long": "first bar of Jan/Aug/Sep/Dec AND close > ema50 AND rsi < 70",
    "short": "first bar of seasonal weak months (Feb/Mar/Jun/Jul) AND close < ema50",
    "desc": "Gold seasonal position: strong months (Jan/Aug/Sep/Dec) confirmed by EMA50+RSI",
    "source": "web:https://fusionmarkets.com/posts/Understanding-Forex-Seasonality",
}

_STRONG_MONTHS = {1, 8, 9, 12}   # historically bullish for XAU
_WEAK_MONTHS = {2, 3, 6, 7}      # seasonal headwinds


def signal(ind, pos, htf=None):
    """Gold seasonal entry with technical filter."""
    ts = ind["open_time"][pos]
    c = ind["close"][pos]
    ema50 = ind["ema50"][pos]
    rsi = ind["rsi"][pos]
    if nan(ts, c, ema50, rsi):
        return None
    ts1 = ind["open_time"][pos - 1]
    if nan(ts1):
        return None
    dt0 = datetime.datetime.utcfromtimestamp(ts / 1000)
    dt1 = datetime.datetime.utcfromtimestamp(ts1 / 1000)
    m0 = dt0.month
    if m0 == dt1.month:
        return None   # not month transition; only enter on first bar of month
    if m0 in _STRONG_MONTHS and c > ema50 and rsi < 70:
        return "long"
    if m0 in _WEAK_MONTHS and c < ema50:
        return "short"
    return None
