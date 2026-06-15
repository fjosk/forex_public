#!/usr/bin/env python3
"""gmma_guppy -- GMMA short-group crosses long-group with EMA200 filter. web:https://www.forexfactory.com/thread/8742-the-ultimate-guppy-multiple-moving-average-gmma-thread"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "gmma_guppy",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "gmma_s, gmma_l, ema200, close",
    "long": "gmma_s crosses above gmma_l AND close > ema200",
    "short": "gmma_s crosses below gmma_l AND close < ema200",
    "desc": "Guppy Multiple Moving Average crossover with EMA200 macro filter",
    "source": "web:https://www.forexfactory.com/thread/8742-the-ultimate-guppy-multiple-moving-average-gmma-thread",
}


def signal(ind, pos, htf=None):
    """GMMA short-group/long-group crossover filtered by EMA200 regime."""
    gs = ind["gmma_s"][pos]
    gs1 = ind["gmma_s"][pos - 1]
    gl = ind["gmma_l"][pos]
    gl1 = ind["gmma_l"][pos - 1]
    e200 = ind["ema200"][pos]
    c = ind["close"][pos]
    if nan(gs, gs1, gl, gl1, e200, c):
        return None
    if _xup(gs, gs1, gl, gl1) and c > e200:
        return "long"
    if _xdn(gs, gs1, gl, gl1) and c < e200:
        return "short"
    return None
