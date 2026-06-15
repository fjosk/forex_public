#!/usr/bin/env python3
"""pin_bar_key_level_daily -- Pin bar at key level daily chart with EMA20 trend alignment. web:dailypriceaction.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pin_bar_key_level_daily",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "open, high, low, close, ema20, body_mom",
    "long": "bullish pin (lower tail >= 2/3 bar range, body <= 25% bar) and close > ema20",
    "short": "bearish pin (upper tail >= 2/3 bar range, body <= 25% bar) and close < ema20",
    "desc": "Pin bar at key level daily chart with EMA20 trend alignment (Justin Bennett style)",
    "source": "web:https://dailypriceaction.com/blog/forex-pin-bar-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Pin bar geometric check with EMA20 trend alignment."""
    o, h, lo, c = ind["open"][pos], ind["high"][pos], ind["low"][pos], ind["close"][pos]
    e20 = ind["ema20"][pos]
    bm = ind["body_mom"][pos]
    if nan(o, h, lo, c, e20, bm):
        return None
    bar_rng = h - lo
    if bar_rng <= 0:
        return None
    body = abs(c - o)
    lower_tail = min(o, c) - lo
    upper_tail = h - max(o, c)
    bull_pin = lower_tail >= 0.67 * bar_rng and body <= 0.25 * bar_rng
    bear_pin = upper_tail >= 0.67 * bar_rng and body <= 0.25 * bar_rng
    if bull_pin and c > e20:
        return "long"
    if bear_pin and c < e20:
        return "short"
    return None
