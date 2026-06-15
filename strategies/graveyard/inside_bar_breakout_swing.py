#!/usr/bin/env python3
"""inside_bar_breakout_swing -- Inside bar volatility breakout swing with EMA200 trend filter. web:priceaction.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_bar_breakout_swing",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "high, low, close, ema200",
    "long": "inside bar at pos-1/pos, trend up (close > ema200), current bar closes above mother bar high",
    "short": "inside bar, trend down (close < ema200), current bar closes below mother bar low",
    "desc": "Inside bar volatility breakout in trend direction with EMA200 filter",
    "source": "web:https://priceaction.com/price-action-university/strategies/pin-bar-inside-bar-combo/",
}


def signal(ind, pos, htf=None):
    """Inside bar detected at pos-1; enter on breakout of mother bar at pos."""
    hi1, lo1 = ind["high"][pos - 1], ind["low"][pos - 1]
    hi2, lo2 = ind["high"][pos - 2], ind["low"][pos - 2]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(hi1, lo1, hi2, lo2, c, e200):
        return None
    inside_bar = hi1 < hi2 and lo1 > lo2
    if not inside_bar:
        return None
    # mother bar is pos-2
    if c > e200 and c > hi2:
        return "long"
    if c < e200 and c < lo2:
        return "short"
    return None
