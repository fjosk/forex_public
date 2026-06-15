#!/usr/bin/env python3
"""inside_bar_daily_breakout -- Inside bar daily breakout in trend direction with EMA50 filter. web:priceaction.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_bar_daily_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "high, low, close, ema50",
    "long": "inside bar at pos-1, trend up (close > ema50), close > mother bar high",
    "short": "inside bar at pos-1, trend down (close < ema50), close < mother bar low",
    "desc": "Inside bar daily chart trend breakout with EMA50 filter (Nial Fuller / PriceAction.com)",
    "source": "web:https://priceaction.com/price-action-university/strategies/inside-bar/",
}


def signal(ind, pos, htf=None):
    """Inside bar trend breakout: mother bar is pos-2, inside bar pos-1, breakout at pos."""
    hi2, lo2 = ind["high"][pos - 2], ind["low"][pos - 2]
    hi1, lo1 = ind["high"][pos - 1], ind["low"][pos - 1]
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    if nan(hi2, lo2, hi1, lo1, c, e50):
        return None
    inside_bar = hi1 < hi2 and lo1 > lo2
    if not inside_bar:
        return None
    if c > e50 and c > hi2:
        return "long"
    if c < e50 and c < lo2:
        return "short"
    return None
