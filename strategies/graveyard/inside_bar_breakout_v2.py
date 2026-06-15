#!/usr/bin/env python3
"""inside_bar_breakout_v2 -- Inside bar breakout (EarnForex): pattern on prior bar, enter on breakout of container. web:earnforex.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_bar_breakout_v2",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "high, low, close, ema200",
    "long": "inside bar (pos-1 inside pos-2), current close breaks above container bar high, trend up",
    "short": "inside bar (pos-1 inside pos-2), current close breaks below container bar low, trend down",
    "desc": "Inside bar breakout: container bar break with EMA200 trend filter (EarnForex style)",
    "source": "web:https://www.earnforex.com/forex-strategy/inside-bar-strategy/",
}


def signal(ind, pos, htf=None):
    """Inside bar breakout on the bar after the pattern completes."""
    hi2, lo2 = ind["high"][pos - 2], ind["low"][pos - 2]   # container/mother bar
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
