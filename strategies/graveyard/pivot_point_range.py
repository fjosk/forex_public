#!/usr/bin/env python3
"""pivot_point_range -- Floor pivot S1/R1 range fade with bounce confirmation. web:babypips.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_point_range",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "piv_s1, piv_r1, low, high, close",
    "long": "prior bar low touched S1, current close closes back above S1 (bounce)",
    "short": "prior bar high touched R1, current close closes back below R1 (rejection)",
    "desc": "Pivot S1/R1 range fade -- prior-bar test then close back on right side",
    "source": "web:https://www.babypips.com/learn/forex/range-trading-with-pivot-points",
}


def signal(ind, pos, htf=None):
    """Pivot range fade: test S1/R1 from proper side, then reverse."""
    s1 = ind["piv_s1"][pos]
    r1 = ind["piv_r1"][pos]
    lo1 = ind["low"][pos - 1]
    hi1 = ind["high"][pos - 1]
    c = ind["close"][pos]
    if nan(s1, r1, lo1, hi1, c):
        return None
    # Long: prior bar dipped to/below S1, current close above S1
    if lo1 <= s1 and c > s1:
        return "long"
    # Short: prior bar spiked to/above R1, current close below R1
    if hi1 >= r1 and c < r1:
        return "short"
    return None
