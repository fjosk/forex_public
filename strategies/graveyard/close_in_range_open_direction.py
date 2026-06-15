#!/usr/bin/env python3
"""close_in_range_open_direction -- Close near high/low of range predicts next-bar direction. trade_your_way_to_financial_freedom_mabroke_blogsp.

If prior bar's close is in the top 30% of its range, expect continuation up; if bottom 30%, expect down.
Uses open-to-close for trend confirmation as well.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "close_in_range_open_direction",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "high,low,close,open",
    "long": "prior bar close in top 30% of range (range_pos >= 0.70) AND close > open",
    "short": "prior bar close in bottom 30% of range (range_pos <= 0.30) AND close < open",
    "desc": "Range-position directional setup: close near bar high/low predicts continuation next bar",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp, Ch7",
}


def signal(ind, pos, htf=None):
    """Close position in range predicts next bar direction."""
    if pos < 1:
        return None
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    if nan(h1, l1, c1, o1):
        return None
    rng1 = h1 - l1
    if rng1 <= 0:
        return None
    rng_pos = (c1 - l1) / rng1
    if rng_pos >= 0.70 and c1 > o1:
        return "long"
    if rng_pos <= 0.30 and c1 < o1:
        return "short"
    return None
