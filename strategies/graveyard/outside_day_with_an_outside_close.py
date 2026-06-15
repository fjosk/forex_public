#!/usr/bin/env python3
"""outside_day_with_an_outside_close -- Outside bar whose close exceeds the prior bar's extreme. trading_systems_and_methods_kaufman_perry_j_kaufma.

An outside day (high[i]>high[i-1] AND low[i]<low[i-1]) where the close extends beyond the
prior bar's extreme: long if close > prior high; short if close < prior low.
Kaufman / Arnold: strong signal when both the range and the close push past the prior extreme.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "outside_day_with_an_outside_close",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close",
    "long": "Outside day AND close > prior day high -> bullish outside close",
    "short": "Outside day AND close < prior day low -> bearish outside close",
    "desc": "Outside day with an outside close: bar range plus close both exceed prior extreme",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Outside day with outside close: range + close both exceed prior extreme."""
    if pos < 1:
        return None
    h  = ind["high"]
    lo = ind["low"]
    c  = ind["close"]
    if nan(h[pos], lo[pos], c[pos], h[pos-1], lo[pos-1]):
        return None

    # Must be an outside bar
    is_outside = h[pos] > h[pos-1] and lo[pos] < lo[pos-1]
    if not is_outside:
        return None

    # Outside close: close extends beyond prior bar's extreme
    if c[pos] > h[pos-1]:
        return "long"
    if c[pos] < lo[pos-1]:
        return "short"

    return None
