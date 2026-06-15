#!/usr/bin/env python3
"""pivot_s1r1_bounce -- intraday bounce off the daily S1/R1 pivot levels. Session class."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_s1r1_bounce",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "piv_s1, piv_r1, low, high, close",
    "long": "bar dipped to S1 then closed back above it",
    "short": "bar spiked to R1 then closed back below it",
    "desc": "Daily-pivot S1/R1 reversion bounce",
    "source": "session-class:floor-trader pivots",
}


def signal(ind, pos, htf=None):
    lo, hi, c = ind["low"][pos], ind["high"][pos], ind["close"][pos]
    s1, r1 = ind["piv_s1"][pos], ind["piv_r1"][pos]
    if nan(lo, hi, c, s1, r1):
        return None
    if lo <= s1 < c:
        return "long"
    if hi >= r1 > c:
        return "short"
    return None
