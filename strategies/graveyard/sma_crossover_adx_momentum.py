#!/usr/bin/env python3
"""sma_crossover_adx_momentum -- SMA5/SMA10 cross with ADX filter and 20-bar momentum. zeta-zetra.

SMA crossover filtered by ADX trend strength plus 20-bar price momentum check.
SMA5 not in indicator set; approximated via close_sma5 (5-bar close average available in engine).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "sma_crossover_adx_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "sma10, adx, close, close_sma5",
    "long": "close_sma5 crosses below SMA10 AND ADX > 20 AND close > close[-20]",
    "short": "close_sma5 crosses above SMA10 AND ADX > 20 AND close < close[-20]",
    "desc": "SMA5/SMA10 crossover with ADX filter and 20-bar momentum check",
    "source": "https://github.com/zeta-zetra/code combination_5.py",
}

_ADX_THRESH = 20.0
_LOOKBACK = 20


def signal(ind, pos, htf=None):
    """SMA5/SMA10 cross filtered by ADX and 20-bar momentum."""
    s5 = ind["close_sma5"][pos]
    s51 = ind["close_sma5"][pos - 1]
    s10 = ind["sma10"][pos]
    s101 = ind["sma10"][pos - 1]
    a = ind["adx"][pos]
    c = ind["close"][pos]
    c20 = ind["close"][pos - _LOOKBACK]
    if nan(s5, s51, s10, s101, a, c, c20):
        return None
    cross_dn = s51 > s101 and s5 < s10   # SMA5 crosses below SMA10 -> spec says LONG
    cross_up = s51 < s101 and s5 > s10   # SMA5 crosses above SMA10 -> spec says SHORT
    if cross_dn and a > _ADX_THRESH and c > c20:
        return "long"
    if cross_up and a > _ADX_THRESH and c < c20:
        return "short"
    return None
