#!/usr/bin/env python3
"""zonal_trading_ao_ac_bill_williams -- AO + AC color agreement zonal entry. MQL4 CodeBase 14512."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "zonal_trading_ao_ac_bill_williams",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ao, ac",
    "long": "AO rising (ao > ao[pos-1]) AND AC rising (ac > ac[pos-1]) -- both green",
    "short": "AO falling (ao < ao[pos-1]) AND AC falling (ac < ac[pos-1]) -- both red",
    "desc": "Bill Williams Zonal Trading: AO and AC both green for long, both red for short",
    "source": "MQL4 Code Base 14512 by rax-1 (Zonal Trading EA, 2016); recommended H4",
}


def signal(ind, pos, htf=None):
    """Both AO and AC must agree in color (sign of bar-to-bar change)."""
    ao_now = ind["ao"][pos]
    ao_prev = ind["ao"][pos - 1]
    ac_now = ind["ac"][pos]
    ac_prev = ind["ac"][pos - 1]
    if nan(ao_now, ao_prev, ac_now, ac_prev):
        return None
    ao_green = ao_now > ao_prev
    ac_green = ac_now > ac_prev
    if ao_green and ac_green:
        return "long"
    if not ao_green and not ac_green:
        return "short"
    return None
