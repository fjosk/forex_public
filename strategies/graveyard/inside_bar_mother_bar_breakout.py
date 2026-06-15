#!/usr/bin/env python3
"""inside_bar_mother_bar_breakout -- Inside Bar breakout: close breaks above/below mother bar extreme.

Detects inside-bar pattern (bar-1 contained within bar-2) and signals when close breaks the mother
bar's extreme. Engine does not support pending stop orders; approximation: signal fires on the bar
that closes beyond the mother bar boundary, so the entry is at the next open (market order).
No volume -> FX-applicable.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_bar_mother_bar_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "open, high, low, close",
    "long": "bar[-1] inside bar[-2]; bar[-2] bearish; bar[-1] bullish; close breaks above bar[-2].high",
    "short": "bar[-1] inside bar[-2]; bar[-2] bullish; bar[-1] bearish; close breaks below bar[-2].low",
    "desc": "Inside bar mother-bar breakout: large-body mother bar with contained inside bar; entry on boundary breach",
    "source": "mql5.com/en/articles/1771 'Automating the Inside Bar Trading Strategy'",
}

# Minimum mother-bar range in price units (approx 800 pips on EUR/USD scale)
_MIN_RANGE = 0.0080


def signal(ind, pos, htf=None):
    """Inside bar breakout: close clears mother bar boundary."""
    if pos < 2:
        return None
    h2 = ind["high"][pos - 2]
    l2 = ind["low"][pos - 2]
    o2 = ind["open"][pos - 2]
    c2 = ind["close"][pos - 2]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    c0 = ind["close"][pos]
    if nan(h2, l2, o2, c2, h1, l1, o1, c1, c0):
        return None
    # Inside bar: bar-1 range contained within bar-2
    is_inside = h1 < h2 and l1 > l2
    if not is_inside:
        return None
    # Mother bar must be large enough
    mother_range = h2 - l2
    if mother_range < _MIN_RANGE:
        return None
    # Long setup: mother bearish (bar-2), inside bullish (bar-1), close breaks above mother high
    mother_bear = o2 > c2
    inside_bull = c1 > o1
    if mother_bear and inside_bull and c0 > h2:
        return "long"
    # Short setup: mother bullish (bar-2), inside bearish (bar-1), close breaks below mother low
    mother_bull = c2 > o2
    inside_bear = c1 < o1
    if mother_bull and inside_bear and c0 < l2:
        return "short"
    return None
