#!/usr/bin/env python3
"""rsi_50_trend_filter_pullback -- RSI 50-level regime with pullback-hook entry. web:wundertrading.com.

RSI above 50 = bullish regime. Wait for RSI to pull back to 40-50 zone and hook upward.
Price above SMA200 adds extra confirmation. No volume dependency.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "rsi_50_trend_filter_pullback",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "rsi, sma200",
    "long": "rsi in 40-50 zone, hooks upward, close > sma200",
    "short": "rsi in 50-60 zone, hooks downward, close < sma200",
    "desc": "RSI 50-level trend filter with pullback-hook entry",
    "source": "web:https://wundertrading.com/journal/en/learn/article/rsi-crossover",
}


def signal(ind, pos, htf=None):
    """RSI regime + pullback hook entry."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    r2 = ind["rsi"][pos - 2]
    c = ind["close"][pos]
    sma = ind["sma200"][pos]
    if nan(r, r1, r2, c, sma):
        return None
    # long: rsi pulled back into 40-50, now hooking up, close above sma200
    if 40 <= r <= 50 and r > r1 and r1 < r2 and c > sma:
        return "long"
    # short: rsi pulled back into 50-60, now hooking down, close below sma200
    if 50 <= r <= 60 and r < r1 and r1 > r2 and c < sma:
        return "short"
    return None
