#!/usr/bin/env python3
"""jackson_gould_five_zone_pivot_day_trade -- Jackson/Gould five-zone day-trade: buy at bottom of zone 3 (between S1 and pivot), sell at top of zone 4. trading_systems_and_methods_kaufman_perry_j_kaufma Ch18."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "jackson_gould_five_zone_pivot_day_trade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "piv_p,piv_r1,piv_s1,close,low,high",
    "long": "Price enters zone 3 (S1 to PP): low <= S1 and close pulls back above S1 toward PP",
    "short": "Price enters zone 4 (PP to R1): high >= R1 and close falls back below R1",
    "desc": "Jackson/Gould zone day-trade: buy zone-3 bottom (near S1), sell zone-4 top (near R1), target the PP",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch18",
}


def signal(ind, pos, htf=None):
    """Long near S1 (bottom of zone 3); short near R1 (top of zone 4); target pivot."""
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
    # Zone 3: between S1 and PP; buy when price dips to S1 and recovers into zone
    if lo <= s1 and s1 < c < pp:
        return "long"
    # Zone 4: between PP and R1; short when price spikes to R1 and falls back into zone
    if hi >= r1 and pp < c < r1:
        return "short"
    return None
