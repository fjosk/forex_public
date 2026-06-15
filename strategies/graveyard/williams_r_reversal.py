#!/usr/bin/env python3
"""williams_r_reversal -- Williams %R zone-exit reversal with EMA200 trend filter. web:quantifiedstrategies.com."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "williams_r_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "willr, ema200",
    "long": "Williams %R crosses above -80 (exits oversold) and close above ema200",
    "short": "Williams %R crosses below -20 (exits overbought) and close below ema200",
    "desc": "Williams %R oversold/overbought zone-exit reversal with EMA200 filter",
    "source": "web:https://www.quantifiedstrategies.com/williams-r-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Williams %R exit from extreme zone, trend-filtered."""
    wr, wr1 = ind["willr"][pos], ind["willr"][pos - 1]
    c, e200 = ind["close"][pos], ind["ema200"][pos]
    if nan(wr, wr1, c, e200):
        return None
    # exit oversold: crosses above -80
    if wr > -80 and wr1 <= -80 and c > e200:
        return "long"
    # exit overbought: crosses below -20
    if wr < -20 and wr1 >= -20 and c < e200:
        return "short"
    return None
