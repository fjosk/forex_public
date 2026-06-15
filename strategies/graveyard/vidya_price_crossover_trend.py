#!/usr/bin/env python3
"""vidya_price_crossover_trend -- VIDYA price crossover with CMO momentum filter. web:quantifiedstrategies.com.

Price crosses above VIDYA while CMO is positive and rising = long. Price crosses below
VIDYA while CMO is negative and falling = short. Hard stop 2x ATR.
No volume dependency.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "vidya_price_crossover_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "vidya, cmo",
    "long": "close crosses above VIDYA AND cmo > 0 AND cmo rising",
    "short": "close crosses below VIDYA AND cmo < 0 AND cmo falling",
    "desc": "VIDYA price crossover with CMO positive/rising filter (Tushar Chande)",
    "source": "web:https://www.quantifiedstrategies.com/variable-index-dynamic-average/",
}


def signal(ind, pos, htf=None):
    """VIDYA price crossover + CMO slope filter."""
    c = ind["close"][pos]
    cp = ind["close"][pos - 1]
    v = ind["vidya"][pos]
    vp = ind["vidya"][pos - 1]
    cmo = ind["cmo"][pos]
    cmop = ind["cmo"][pos - 1]
    if nan(c, cp, v, vp, cmo, cmop):
        return None
    cross_above = c > v and cp <= vp
    cross_below = c < v and cp >= vp
    cmo_pos_rising = cmo > 0 and cmo > cmop
    cmo_neg_falling = cmo < 0 and cmo < cmop
    if cross_above and cmo_pos_rising:
        return "long"
    if cross_below and cmo_neg_falling:
        return "short"
    return None
