#!/usr/bin/env python3
"""gmma_guppy_trend_filter -- GMMA Guppy MMA crossover with fan confirmation. StockCharts/Babypips.

Two EMA groups: short composite (gmma_s) and long composite (gmma_l). Enter on crossover when
spread is widening (both groups fanning apart). Exit on reverse crossover.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "gmma_guppy_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "gmma_s, gmma_l (Guppy short/long EMA group composites)",
    "long": "gmma_s crosses above gmma_l and spread is widening",
    "short": "gmma_s crosses below gmma_l and spread is widening downward",
    "desc": "Guppy Multiple Moving Average crossover with fan confirmation",
    "source": "web:https://chartschool.stockcharts.com; https://www.babypips.com/learn/forex/guppy-multiple-moving-average",
}


def signal(ind, pos, htf=None):
    """GMMA Guppy crossover with fan confirmation."""
    gs = ind["gmma_s"][pos]
    gl = ind["gmma_l"][pos]
    gs1 = ind["gmma_s"][pos - 1]
    gl1 = ind["gmma_l"][pos - 1]
    if nan(gs, gl, gs1, gl1):
        return None
    # spread now vs 3 bars ago for fanning check
    if pos < 4:
        return None
    gs3 = ind["gmma_s"][pos - 3]
    gl3 = ind["gmma_l"][pos - 3]
    if nan(gs3, gl3):
        return None
    spread_now = gs - gl
    spread_prev = gs3 - gl3
    # long: cross above with widening positive spread
    if _xup(gs, gs1, gl, gl1) and spread_now > spread_prev:
        return "long"
    # short: cross below with widening negative spread
    if _xdn(gs, gs1, gl, gl1) and spread_now < spread_prev:
        return "short"
    return None
