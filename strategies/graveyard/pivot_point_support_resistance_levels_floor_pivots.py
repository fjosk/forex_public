#!/usr/bin/env python3
"""pivot_point_support_resistance_levels_floor_pivots -- Floor pivots S1/R1 bias entry: long above P near S1, short below P near R1. j_person_a_complete_guide_to_technical_trading_tac Ch6."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_point_support_resistance_levels_floor_pivots",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "piv_p,piv_r1,piv_s1,close,low,high",
    "long": "Long bias above P; buy near S1 support (price dips to S1 and recovers)",
    "short": "Short bias below P; sell near R1 resistance (price rallies to R1 and retreats)",
    "desc": "Classic floor pivot: P = bias line; long above P on S1 support; short below P on R1 resistance",
    "source": "book: j_person_a_complete_guide_to_technical_trading_tac, Ch6",
}


def signal(ind, pos, htf=None):
    """Long on S1 bounce with bullish pivot bias; short on R1 rejection with bearish pivot bias."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    pp = ind["piv_p"][pos]
    r1 = ind["piv_r1"][pos]
    s1 = ind["piv_s1"][pos]
    if nan(c, lo, hi, pp, r1, s1):
        return None
    if c > pp and lo <= s1 and c > s1:
        return "long"
    if c < pp and hi >= r1 and c < r1:
        return "short"
    return None
