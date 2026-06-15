#!/usr/bin/env python3
"""macd_zero_cross_trend_follow -- MACD zero-line crossover with ADX trending filter. web:https://commodity.com/technical-analysis/macd/"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_zero_cross_trend_follow",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd, macd_hist, adx",
    "long": "MACD crosses zero from below AND ADX >= 20 AND histogram positive",
    "short": "MACD crosses zero from above AND ADX >= 20 AND histogram negative",
    "desc": "MACD zero-line cross trend follower with ADX trending-market filter",
    "source": "web:https://commodity.com/technical-analysis/macd/",
}


def signal(ind, pos, htf=None):
    """MACD zero-line cross filtered by ADX minimum trend strength."""
    macd = ind["macd"][pos]
    macd1 = ind["macd"][pos - 1]
    hist = ind["macd_hist"][pos]
    adx = ind["adx"][pos]
    if nan(macd, macd1, hist, adx):
        return None
    trending = adx >= 20
    cross_up = macd > 0 and macd1 <= 0
    cross_dn = macd < 0 and macd1 >= 0
    if cross_up and trending and hist > 0:
        return "long"
    if cross_dn and trending and hist < 0:
        return "short"
    return None
