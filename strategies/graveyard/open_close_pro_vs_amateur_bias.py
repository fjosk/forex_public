#!/usr/bin/env python3
"""open_close_pro_vs_amateur_bias -- Close vs open + close-position-in-range directional bias. elder_alexander_trading_for_a_living.

Bar close > open AND close in upper 70% of range -> professionals were bullish -> long.
Bar close < open AND close in lower 30% of range -> professionals were bearish -> short.
Requires both signals on two consecutive bars for confirmation.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "open_close_pro_vs_amateur_bias",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "open,high,low,close",
    "long": "close > open AND close in upper 70% of bar range (professionals bought the bar) on both last 2 bars",
    "short": "close < open AND close in lower 30% of bar range (professionals sold the bar) on both last 2 bars",
    "desc": "Pro/amateur open-close bias: professionals dominate close; two confirming bars required",
    "source": "elder_alexander_trading_for_a_living, Sec18 Charting",
}


def signal(ind, pos, htf=None):
    """Open-close pro/amateur bias with 2-bar confirmation."""
    if pos < 2:
        return None
    bull_bars = 0
    bear_bars = 0
    for k in [pos - 1, pos]:
        o = ind["open"][k]
        h = ind["high"][k]
        l = ind["low"][k]
        c = ind["close"][k]
        if nan(o, h, l, c):
            return None
        rng = h - l
        if rng <= 0:
            return None
        rng_pos = (c - l) / rng
        if c > o and rng_pos >= 0.70:
            bull_bars += 1
        elif c < o and rng_pos <= 0.30:
            bear_bars += 1
    if bull_bars == 2:
        return "long"
    if bear_bars == 2:
        return "short"
    return None
