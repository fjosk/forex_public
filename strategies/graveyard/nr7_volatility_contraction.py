#!/usr/bin/env python3
"""nr7_volatility_contraction -- NR7 narrow range bar breakout (Linda Raschke). web:stockcharts.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "nr7_volatility_contraction",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "high, low",
    "long": "NR7 bar on prior bar (smallest range of 7), current high breaks above NR7 high",
    "short": "NR7 bar on prior bar, current low breaks below NR7 low",
    "desc": "NR7 narrow range volatility contraction breakout (Raschke/Crabel)",
    "source": "web:https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/narrow-range-day-nr7",
}

_NR_PERIOD = 7


def signal(ind, pos, htf=None):
    """NR7: prior bar range is the smallest of 7 bars; break above/below triggers entry."""
    if pos < _NR_PERIOD:
        return None
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    hi1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    if nan(hi, lo, hi1, lo1):
        return None
    # check NR7 condition on the prior bar
    prior_range = hi1 - lo1
    if prior_range <= 0:
        return None
    for i in range(2, _NR_PERIOD):
        h = ind["high"][pos - i]
        l = ind["low"][pos - i]
        if nan(h, l):
            return None
        if (h - l) <= prior_range:
            return None  # prior bar is NOT the narrowest
    # prior bar is NR7; check breakout on current bar
    if hi > hi1:
        return "long"
    if lo < lo1:
        return "short"
    return None
