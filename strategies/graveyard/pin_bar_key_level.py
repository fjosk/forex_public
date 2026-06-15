#!/usr/bin/env python3
"""pin_bar_key_level -- Pin bar (Nial Fuller) at fractal or pivot S/R level. web:dailypriceaction.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pin_bar_key_level",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "open, high, low, close, piv_s1, piv_r1, frac_dn_px, frac_up_px, atr",
    "long": "bullish pin bar (lower tail > 66% of range) at fractal support or piv_s1",
    "short": "bearish pin bar (upper tail > 66% of range) at fractal resistance or piv_r1",
    "desc": "Pin bar at fractal or pivot key level (Nial Fuller style)",
    "source": "web:https://dailypriceaction.com/blog/forex-pin-bar-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Pin bar at fractal/pivot S/R proximity."""
    o, h, lo, c = ind["open"][pos], ind["high"][pos], ind["low"][pos], ind["close"][pos]
    s1, r1 = ind["piv_s1"][pos], ind["piv_r1"][pos]
    fdn, fup = ind["frac_dn_px"][pos], ind["frac_up_px"][pos]
    atr = ind["atr"][pos]
    if nan(o, h, lo, c, s1, r1, fdn, fup, atr):
        return None
    if atr <= 0:
        return None
    bar_rng = h - lo
    if bar_rng <= 0:
        return None
    body = abs(c - o)
    lower_tail = min(o, c) - lo
    upper_tail = h - max(o, c)
    bull_pin = lower_tail > 0.66 * bar_rng and body < 0.33 * bar_rng
    bear_pin = upper_tail > 0.66 * bar_rng and body < 0.33 * bar_rng
    pip5 = atr * 0.25
    at_support = lo <= s1 + pip5 or lo <= fdn + pip5
    at_resist = h >= r1 - pip5 or h >= fup - pip5
    if bull_pin and at_support:
        return "long"
    if bear_pin and at_resist:
        return "short"
    return None
