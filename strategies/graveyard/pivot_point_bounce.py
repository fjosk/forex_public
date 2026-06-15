#!/usr/bin/env python3
"""pivot_point_bounce -- Floor pivot S1/R1 bounce with day_open bias filter. web:forexfactory.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_point_bounce",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "piv_s1, piv_r1, piv_p, day_open, low, high, close, open",
    "long": "opened above pivot P, prior bar tested S1, current close reclaims above S1",
    "short": "opened below pivot P, prior bar tested R1, current close falls back below R1",
    "desc": "Floor pivot S1/R1 rejection bounce with day-open bias",
    "source": "web:https://www.forexfactory.com/thread/2961-trading-with-pivot-points",
}


def signal(ind, pos, htf=None):
    """Pivot bounce: price tests S1/R1, rejects and closes back on bias side."""
    s1, r1, pp = ind["piv_s1"][pos], ind["piv_r1"][pos], ind["piv_p"][pos]
    do = ind["day_open"][pos]
    lo1, hi1, c1 = ind["low"][pos - 1], ind["high"][pos - 1], ind["close"][pos - 1]
    c = ind["close"][pos]
    if nan(s1, r1, pp, do, lo1, hi1, c1, c):
        return None
    # Long: opened above pivot, prior bar dipped to/below S1 then current close is above S1
    if do > pp and lo1 <= s1 and c > s1:
        return "long"
    # Short: opened below pivot, prior bar spiked to/above R1 then current close is below R1
    if do < pp and hi1 >= r1 and c < r1:
        return "short"
    return None
