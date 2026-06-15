#!/usr/bin/env python3
"""bollinger_bands_breakout_earnforex -- BB breakout EA: close crosses outside BB band. web:earnforex.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bollinger_bands_breakout_earnforex",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "bb_up, bb_lo, close",
    "long": "prior close <= bb_up, current close > bb_up (BB upper breakout)",
    "short": "prior close >= bb_lo, current close < bb_lo (BB lower breakout)",
    "desc": "Bollinger Bands breakout EA: close crosses outside upper or lower BB (EarnForex)",
    "source": "web:https://www.earnforex.com/metatrader-expert-advisors/bollinger-bands-breakout/",
}


def signal(ind, pos, htf=None):
    """BB breakout: close crosses above bb_up or below bb_lo."""
    cl = ind["close"][pos]
    cl1 = ind["close"][pos - 1]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up1 = ind["bb_up"][pos - 1]
    bb_lo1 = ind["bb_lo"][pos - 1]
    if nan(cl, cl1, bb_up, bb_lo, bb_up1, bb_lo1):
        return None
    if cl > bb_up and cl1 <= bb_up1:
        return "long"
    if cl < bb_lo and cl1 >= bb_lo1:
        return "short"
    return None
