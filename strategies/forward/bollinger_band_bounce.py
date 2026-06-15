#!/usr/bin/env python3
"""bollinger_band_bounce -- Bollinger Band pierce-and-return mean reversion with RSI context. web:tradingpedia.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bollinger_band_bounce",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_lo, bb_up, rsi",
    "long": "prior close below bb_lo, current close back above bb_lo, RSI > 50",
    "short": "prior close above bb_up, current close back below bb_up, RSI < 50",
    "desc": "Bollinger Band bounce: pierce-and-return with RSI trend context",
    "source": "web:https://www.tradingpedia.com/forex-trading-strategies/forex-trading-strategy-relative-strength-index-bollinger-bands/",
}


def signal(ind, pos, htf=None):
    """BB pierce-and-return: close crosses back inside from the outer band."""
    cl = ind["close"][pos]
    cl1 = ind["close"][pos - 1]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up1 = ind["bb_up"][pos - 1]
    bb_lo1 = ind["bb_lo"][pos - 1]
    rsi = ind["rsi"][pos]
    if nan(cl, cl1, bb_up, bb_lo, bb_up1, bb_lo1, rsi):
        return None
    # long: prior close below lower band, current close back above
    if cl1 < bb_lo1 and cl > bb_lo and rsi > 50:
        return "long"
    # short: prior close above upper band, current close back below
    if cl1 > bb_up1 and cl < bb_up and rsi < 50:
        return "short"
    return None
