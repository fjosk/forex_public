#!/usr/bin/env python3
"""inside_bar_trend_breakout -- Inside bar mother bar breakout in EMA200 trend direction. web:strategyquant.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_bar_trend_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "high, low, close, ema200",
    "long": "inside bar formed at pos-1 (inside pos-2 mother), current close > mother high and above EMA200",
    "short": "inside bar formed at pos-1, current close < mother low and below EMA200",
    "desc": "Inside bar trend breakout (StrategyQuant style) -- EMA200 trend gate",
    "source": "web:https://strategyquant.com/blog/inside-bar-breakout-strategy-price-action-trading/",
}


def signal(ind, pos, htf=None):
    """Inside bar breakout with EMA200 trend confirmation (StrategyQuant variant)."""
    hi2, lo2 = ind["high"][pos - 2], ind["low"][pos - 2]   # mother bar
    hi1, lo1 = ind["high"][pos - 1], ind["low"][pos - 1]   # inside bar
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(hi2, lo2, hi1, lo1, c, e200):
        return None
    inside_formed = hi1 < hi2 and lo1 > lo2
    if not inside_formed:
        return None
    if c > e200 and c > hi2:
        return "long"
    if c < e200 and c < lo2:
        return "short"
    return None
