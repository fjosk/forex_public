#!/usr/bin/env python3
"""floyd_pivot_point_support_resistance_projection -- Floyd/classic pivot point buy near S1/S2, sell near R1/R2. trading_systems_and_methods_kaufman_perry_j_kaufma Ch15."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "floyd_pivot_point_support_resistance_projection",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "piv_p,piv_r1,piv_s1,piv_r2,piv_s2,close,low,high",
    "long": "Price touches or dips below S1 then closes back above S1 (S1 support hold)",
    "short": "Price touches or rises above R1 then closes back below R1 (R1 resistance hold)",
    "desc": "Classic Floyd pivot-point S/R reaction entry: buy S1/S2 bounce, sell R1/R2 rejection",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch15",
}


def signal(ind, pos, htf=None):
    """Long on S1 support bounce; short on R1 resistance rejection."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    pp = ind["piv_p"][pos]
    r1 = ind["piv_r1"][pos]
    s1 = ind["piv_s1"][pos]
    if nan(c, c1, lo, hi, pp, r1, s1):
        return None
    # Long: price is near or above pivot (above S1), tests S1 and closes back above
    if lo <= s1 and c > s1:
        return "long"
    # Short: price tests R1 and closes back below it
    if hi >= r1 and c < r1:
        return "short"
    return None
