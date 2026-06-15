#!/usr/bin/env python3
"""nr7_volatility_contraction_breakout -- NR7 narrow range breakout with SMA100 trend filter. web:forextraininggroup."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "nr7_volatility_contraction_breakout",
    "cadences": ["swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1d",
    "indicators": "high, low, close, sma100",
    "long": "today is NR7 (narrowest range in 7 bars) and close above SMA100",
    "short": "today is NR7 and close below SMA100",
    "desc": "Crabel NR7 narrow range bar breakout filtered by SMA100 trend direction",
    "source": "web:https://forextraininggroup.com/simple-tactics-for-trading-narrow-range-bars-nr4-nr7-nr4id/",
}

_NR_WINDOW = 7


def signal(ind, pos, htf=None):
    """NR7 volatility contraction breakout."""
    h = ind["high"][pos]
    lo = ind["low"][pos]
    c = ind["close"][pos]
    s100 = ind["sma100"][pos]
    if nan(h, lo, c, s100):
        return None
    if pos < _NR_WINDOW:
        return None
    bar_range = h - lo
    # Check this bar's range is the smallest of the last 7 bars
    for i in range(pos - _NR_WINDOW + 1, pos):
        h_i = ind["high"][i]
        l_i = ind["low"][i]
        if nan(h_i, l_i):
            return None
        if (h_i - l_i) < bar_range:
            return None  # not NR7 -- a prior bar is narrower
    # NR7 confirmed
    if c > s100:
        return "long"
    if c < s100:
        return "short"
    return None
