#!/usr/bin/env python3
"""adx_di_crossover -- Classic Wilder ADX DI crossover >= 25. TradingPedia.

+DI crosses above -DI with ADX >= 25 = long. -DI crosses above +DI with ADX >= 25 = short.
The clean Wilder DMI system, no extra filters beyond the strength threshold.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "adx_di_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "adx, di_plus, di_minus",
    "long": "+DI crosses above -DI and ADX >= 25",
    "short": "-DI crosses above +DI and ADX >= 25",
    "desc": "Classic Wilder DMI DI crossover with ADX >= 25 trend strength filter",
    "source": "web:https://www.tradingpedia.com/forex-academy/average-directional-movement-index/",
}


def signal(ind, pos, htf=None):
    """Wilder DI cross + ADX threshold."""
    adx_v = ind["adx"][pos]
    dp = ind["di_plus"][pos]
    dm = ind["di_minus"][pos]
    dp1 = ind["di_plus"][pos - 1]
    dm1 = ind["di_minus"][pos - 1]
    if nan(adx_v, dp, dm, dp1, dm1):
        return None
    if adx_v < 25:
        return None
    if _xup(dp, dp1, dm, dm1):
        return "long"
    if _xdn(dp, dp1, dm, dm1):
        return "short"
    return None
