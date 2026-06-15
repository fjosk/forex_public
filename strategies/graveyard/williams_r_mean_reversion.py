#!/usr/bin/env python3
"""williams_r_mean_reversion -- Williams %R extreme oversold/overbought reversion. QuantifiedStrategies."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "williams_r_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "daily",
    "indicators": "willr, high, close",
    "long": "Williams %R < -90 (extreme oversold)",
    "short": "Williams %R > -10 (extreme overbought)",
    "desc": "Williams %R extreme entry: buy at -90 oversold, sell at -10 overbought",
    "source": "web:https://www.quantifiedstrategies.com/williams-r-strategy/",
}


def signal(ind, pos, htf=None):
    """Williams %R extreme: enter long below -90, short above -10."""
    wr = ind["willr"][pos]
    c = ind["close"][pos]
    if nan(wr, c):
        return None

    if wr < -90:
        return "long"
    if wr > -10:
        return "short"

    return None
