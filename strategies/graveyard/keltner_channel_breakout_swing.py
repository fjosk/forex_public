#!/usr/bin/env python3
"""keltner_channel_breakout_swing -- Keltner Channel breakout with ADX > 25 filter. web:quantifiedstrategies.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "keltner_channel_breakout_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "kc_up, kc_lo, adx",
    "long": "ADX > 25 and close > kc_up",
    "short": "ADX > 25 and close < kc_lo",
    "desc": "Keltner Channel breakout swing entry with ADX > 25 trend filter",
    "source": "web:https://www.quantifiedstrategies.com/keltner-bands-trading-strategies/",
}


def signal(ind, pos, htf=None):
    """KC breakout: ADX > 25 and close outside Keltner band."""
    cl = ind["close"][pos]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    adx = ind["adx"][pos]
    if nan(cl, kc_up, kc_lo, adx):
        return None
    if adx <= 25:
        return None
    if cl > kc_up:
        return "long"
    if cl < kc_lo:
        return "short"
    return None
