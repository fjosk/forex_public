#!/usr/bin/env python3
"""pin_bar_inside_bar -- Pin bar and inside bar dual price-action setup. web:dailypriceaction.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pin_bar_inside_bar",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "open, high, low, close, atr, piv_s1, piv_r1",
    "long": "bullish pin bar (lower wick >= 2x body) near piv_s1 support OR inside bar breakout above mother high",
    "short": "bearish pin bar (upper wick >= 2x body) near piv_r1 resistance OR inside bar breakout below mother low",
    "desc": "Combined pin bar and inside bar price-action entry at pivot S/R",
    "source": "web:https://dailypriceaction.com/blog/forex-pin-bar-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Pin bar at pivot S/R or inside bar breakout above/below mother."""
    o, h, lo, c = ind["open"][pos], ind["high"][pos], ind["low"][pos], ind["close"][pos]
    atr = ind["atr"][pos]
    s1, r1 = ind["piv_s1"][pos], ind["piv_r1"][pos]
    hi1, lo1 = ind["high"][pos - 1], ind["low"][pos - 1]
    hi2, lo2 = ind["high"][pos - 2], ind["low"][pos - 2]
    c1 = ind["close"][pos - 1]
    if nan(o, h, lo, c, atr, s1, r1, hi1, lo1, hi2, lo2, c1):
        return None
    if atr <= 0:
        return None
    body = abs(c - o)
    lower_wick = min(o, c) - lo
    upper_wick = h - max(o, c)
    # Pin bar logic
    bull_pin = lower_wick >= 2 * body and upper_wick < body * 0.5 if body > 0 else False
    bear_pin = upper_wick >= 2 * body and lower_wick < body * 0.5 if body > 0 else False
    near_s1 = c <= s1 + atr * 0.5
    near_r1 = c >= r1 - atr * 0.5
    # Inside bar breakout logic (current bar breaks out of pos-2 mother when pos-1 was inside)
    ib_prev = hi1 < hi2 and lo1 > lo2
    if bull_pin and near_s1:
        return "long"
    if bear_pin and near_r1:
        return "short"
    if ib_prev and c > hi2:
        return "long"
    if ib_prev and c < lo2:
        return "short"
    return None
