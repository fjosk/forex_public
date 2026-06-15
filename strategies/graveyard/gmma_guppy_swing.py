#!/usr/bin/env python3
"""gmma_guppy_swing -- GMMA Guppy pullback to long-group zone. web:https://www.babypips.com/learn/forex/guppy-multiple-moving-average"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "gmma_guppy_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "gmma_s, gmma_l, atr, close, open",
    "long": "gmma_s > gmma_l (bull), price pulls back near gmma_l, bullish candle",
    "short": "gmma_s < gmma_l (bear), price rallies near gmma_l, bearish candle",
    "desc": "GMMA Guppy pullback to long-group zone in confirmed trend",
    "source": "web:https://www.babypips.com/learn/forex/guppy-multiple-moving-average",
}


def signal(ind, pos, htf=None):
    """GMMA short-group above long-group trend, pullback entry near long-group."""
    gs = ind["gmma_s"][pos]
    gl = ind["gmma_l"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    atr = ind["atr"][pos]
    if nan(gs, gl, c, o, atr):
        return None
    bull_trend = gs > gl
    bear_trend = gs < gl
    near_long_group = abs(c - gl) < atr
    bull_candle = c > o
    bear_candle = c < o
    if bull_trend and near_long_group and bull_candle:
        return "long"
    if bear_trend and near_long_group and bear_candle:
        return "short"
    return None
