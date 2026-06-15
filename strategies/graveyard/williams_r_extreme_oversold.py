#!/usr/bin/env python3
"""williams_r_extreme_oversold -- Williams %R extreme oversold/overbought mean-reversion. web:quantifiedstrategies.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "williams_r_extreme_oversold",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "willr, high, low",
    "long": "Williams %R drops below -90 (extreme oversold)",
    "short": "Williams %R rises above -10 (extreme overbought)",
    "desc": "Williams %R extreme zone entry for mean-reversion",
    "source": "web:https://quantifiedstrategies.substack.com/p/williams-percent-r-indicator",
}


def signal(ind, pos, htf=None):
    """Williams %R extreme oversold/overbought entry."""
    wr = ind["willr"][pos]
    if nan(wr):
        return None
    if wr < -90:
        return "long"
    if wr > -10:
        return "short"
    return None
