#!/usr/bin/env python3
"""wide_range_bar_vol_entry_filter -- Wide-range-bar volatility entry filter: only take a breakout when the event bar's range exceeds the 20-bar average range; bars with 2x+ average range are strongest. Bulkowski Encyclopedia Ch.60-63.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "wide_range_bar_vol_entry_filter",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "high, low, close, rng_sma20",
    "long": "Prior bar range > rng_sma20 (wide range) and today close breaks above prior bar high",
    "short": "Prior bar range > rng_sma20 (wide range) and today close breaks below prior bar low",
    "desc": "Wide-range-bar filter: event bar with above-average daily range improves breakout performance; only take breakout when bar is wide",
    "source": "encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bulkowski -- Ch.60-63 Large price range guideline tables 60.1-63.1",
}


def signal(ind, pos, htf=None):
    """Wide prior bar then close breaks out of it in either direction."""
    if pos < 1:
        return None
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c = ind["close"][pos]
    avg_rng = ind["rng_sma20"][pos]
    if nan(h1, l1, c, avg_rng):
        return None
    if avg_rng <= 0:
        return None
    bar_range = h1 - l1
    if bar_range <= avg_rng:
        return None  # not a wide bar, skip
    if c > h1:
        return "long"
    if c < l1:
        return "short"
    return None
