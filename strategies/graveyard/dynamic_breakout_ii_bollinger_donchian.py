#!/usr/bin/env python3
"""dynamic_breakout_ii_bollinger_donchian -- BB + Donchian adaptive breakout (QuantConnect). web:quantconnect.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "dynamic_breakout_ii_bollinger_donchian",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "bb_up, bb_lo, hh_n, ll_n, close",
    "long": "prior close > bb_up and current close > hh_n",
    "short": "prior close < bb_lo and current close < ll_n",
    "desc": "Dynamic Breakout II: prior close outside BB, current close beyond N-bar Donchian extreme (QC)",
    "source": "web:https://www.quantconnect.com/learning/articles/investment-strategy-library/the-dynamic-breakout-ii-strategy",
}


def signal(ind, pos, htf=None):
    """Dynamic Breakout II: prior BB exit confirms Donchian breakout on current bar."""
    cl = ind["close"][pos]
    cl1 = ind["close"][pos - 1]
    bb_up1 = ind["bb_up"][pos - 1]
    bb_lo1 = ind["bb_lo"][pos - 1]
    hhn = ind["hh_n"][pos]
    lln = ind["ll_n"][pos]
    if nan(cl, cl1, bb_up1, bb_lo1, hhn, lln):
        return None
    if cl1 > bb_up1 and cl > hhn:
        return "long"
    if cl1 < bb_lo1 and cl < lln:
        return "short"
    return None
