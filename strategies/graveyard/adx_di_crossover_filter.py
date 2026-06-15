#!/usr/bin/env python3
"""adx_di_crossover_filter -- ADX DI+/DI- crossover with ADX>25 rising filter. ForexFactory ADXB.

DI+ crosses above DI- with ADX above 25 and rising = long trend start.
DI- crosses above DI+ with same conditions = short. Exit on opposite DI cross or ADX<20.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "adx_di_crossover_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "adx, di_plus, di_minus, atr",
    "long": "DI+ crosses above DI- with ADX > 25 and ADX rising",
    "short": "DI- crosses above DI+ with ADX > 25 and ADX rising",
    "desc": "ADX DI crossover trend entry with ADX strength and slope filter",
    "source": "web:https://www.forexfactory.com/thread/595717-adxb-a-trend-following-strategy-ea",
}


def signal(ind, pos, htf=None):
    """DI cross + ADX strength + rising slope."""
    adx_v = ind["adx"][pos]
    adx1 = ind["adx"][pos - 1]
    dp = ind["di_plus"][pos]
    dm = ind["di_minus"][pos]
    dp1 = ind["di_plus"][pos - 1]
    dm1 = ind["di_minus"][pos - 1]
    if nan(adx_v, adx1, dp, dm, dp1, dm1):
        return None
    if adx_v < 25 or adx_v <= adx1:
        return None  # weak or not rising
    if _xup(dp, dp1, dm, dm1):
        return "long"
    if _xdn(dp, dp1, dm, dm1):
        return "short"
    return None
