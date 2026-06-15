#!/usr/bin/env python3
"""pin_bar_at_sr_daily -- Pin bar at key S/R level (fractal or SMA200 proximity). web:dailypriceaction.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pin_bar_at_sr_daily",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "open, high, low, close, atr, sma200, frac_dn_px, frac_up_px",
    "long": "bullish pin bar (lower tail >= 2/3 bar, small body) near fractal support or SMA200",
    "short": "bearish pin bar (upper tail >= 2/3 bar, small body) near fractal resistance or SMA200",
    "desc": "Pin bar at key S/R (fractal or SMA200) on daily chart",
    "source": "web:https://dailypriceaction.com/blog/forex-pin-bar-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Pin bar at S/R: geometric check + fractal/SMA200 proximity."""
    o, h, lo, c = ind["open"][pos], ind["high"][pos], ind["low"][pos], ind["close"][pos]
    atr = ind["atr"][pos]
    sma200 = ind["sma200"][pos]
    fdn = ind["frac_dn_px"][pos]
    fup = ind["frac_up_px"][pos]
    if nan(o, h, lo, c, atr, sma200, fdn, fup):
        return None
    if atr <= 0:
        return None
    bar_rng = h - lo
    if bar_rng <= 0:
        return None
    body = abs(c - o)
    lower_tail = min(o, c) - lo
    upper_tail = h - max(o, c)
    # Bullish pin: lower tail >= 2/3 bar, body < 1/3 bar
    bull_pin = lower_tail >= 0.67 * bar_rng and body < 0.33 * bar_rng
    # Bearish pin: upper tail >= 2/3 bar, body < 1/3 bar
    bear_pin = upper_tail >= 0.67 * bar_rng and body < 0.33 * bar_rng
    at_support = abs(lo - fdn) < atr or abs(lo - sma200) < atr
    at_resist = abs(h - fup) < atr or abs(h - sma200) < atr
    if bull_pin and at_support:
        return "long"
    if bear_pin and at_resist:
        return "short"
    return None
