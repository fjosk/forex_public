#!/usr/bin/env python3
"""inside_bar_pending_order_ea -- Inside bar breakout: current bar inside prior bar's range. MQL4."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_bar_pending_order_ea",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "high, low, atr",
    "long": "inside bar detected (pos high < pos-1 high AND pos low > pos-1 low); next bar breaks above mother high",
    "short": "inside bar; break below mother low",
    "desc": "Inside bar pending order: identify inside bar then trade the breakout of the mother bar range",
    "source": "web:https://www.mql5.com/en/articles/1771",
}

_MIN_ATR_MULT = 0.5   # mother bar must be at least 0.5 ATR to avoid flat-market noise


def signal(ind, pos, htf=None):
    """Inside bar at pos-1 -> breakout at pos above/below the mother bar (pos-2)."""
    # At pos, check if pos-1 was an inside bar (contained within pos-2)
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    h2 = ind["high"][pos - 2]
    l2 = ind["low"][pos - 2]
    c = ind["close"][pos]
    atr = ind["atr"][pos]
    if nan(h1, l1, h2, l2, c, atr):
        return None
    mother_range = h2 - l2
    if mother_range < _MIN_ATR_MULT * atr:
        return None
    inside = h1 < h2 and l1 > l2
    if not inside:
        return None
    # Current bar closes above mother high = long breakout
    if c > h2:
        return "long"
    if c < l2:
        return "short"
    return None
