#!/usr/bin/env python3
"""adx_di_crossover_trend_follow -- ADX DI Crossover Trend Following EA.
web:https://www.mql5.com/en/code/22830
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "adx_di_crossover_trend_follow",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "any",
    "indicators": "adx, di_plus, di_minus",
    "long": "DI+ crosses above DI- AND ADX >= 25",
    "short": "DI+ crosses below DI- AND ADX >= 25",
    "desc": "DI+/DI- crossover with ADX strength gate confirming sufficient trend momentum",
    "source": "web:https://www.mql5.com/en/code/22830",
}


def signal(ind, pos, htf=None):
    """DI crossover with ADX trend-strength filter (ADX >= 25)."""
    adx = ind["adx"][pos]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    dip1 = ind["di_plus"][pos - 1]
    dim1 = ind["di_minus"][pos - 1]
    if nan(adx, dip, dim, dip1, dim1):
        return None
    if adx < 25:
        return None
    if _xup(dip, dip1, dim, dim1):
        return "long"
    if _xdn(dip, dip1, dim, dim1):
        return "short"
    return None
