#!/usr/bin/env python3
"""tall_pattern_height_filter -- Tall-pattern height filter: take a breakout only when the event bar's range-to-price ratio exceeds the median (~5.5%); skip short patterns. Bulkowski Encyclopedia of Chart Patterns Ch.60-63.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "tall_pattern_height_filter",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "high, low, close, atr_pct",
    "long": "Range/close >= 0.055 (tall bar) and close breaks above bar high[1]",
    "short": "Range/close >= 0.055 (tall bar) and close breaks below bar low[1]",
    "desc": "Tall-pattern height filter: breakout only when event bar height-percent exceeds the historical median of ~5.5%",
    "source": "encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bulkowski -- Ch.60-63 Size and Volume Statistics tables 60.6-63.6",
}

# Historical median height percent from Bulkowski tables (5.2-6.9%); use 5.5% midpoint
_HEIGHT_THRESHOLD = 0.055


def signal(ind, pos, htf=None):
    """Enter breakout only when prior bar was a tall bar by Bulkowski median standard."""
    if pos < 1:
        return None
    # Event bar = prior bar (pos-1); today's close confirms the breakout
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c = ind["close"][pos]
    if nan(h1, l1, c):
        return None
    if l1 <= 0:
        return None
    height_pct = (h1 - l1) / l1
    if height_pct < _HEIGHT_THRESHOLD:
        return None  # short pattern, skip
    # Breakout: today's close clears the event bar's high (long) or low (short)
    if c > h1:
        return "long"
    if c < l1:
        return "short"
    return None
