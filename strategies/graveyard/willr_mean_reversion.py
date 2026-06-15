#!/usr/bin/env python3
"""willr_mean_reversion -- Williams %R extreme re-cross mean reversion. QuantifiedStrategies / Larry Williams.

Long when %R crosses back above -80 (exiting oversold zone).
Short when %R crosses back below -20 (exiting overbought zone).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "willr_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "daily",
    "indicators": "willr, sma200",
    "long": "willr crosses back above -80 (from oversold) and close > SMA200",
    "short": "willr crosses back below -20 (from overbought) and close < SMA200",
    "desc": "Williams %R extreme zone re-cross mean reversion",
    "source": "web:https://www.quantifiedstrategies.com/williams-r-strategy/; Larry Williams (1999)",
}


def signal(ind, pos, htf=None):
    """Williams %R re-cross out of extreme zone."""
    w = ind["willr"][pos]
    w1 = ind["willr"][pos - 1]
    s200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(w, w1, s200, c):
        return None
    if w > -80 and w1 <= -80 and c > s200:
        return "long"
    if w < -20 and w1 >= -20 and c < s200:
        return "short"
    return None
