#!/usr/bin/env python3
"""gmma_ribbon_crossover_compression -- GMMA short/long ribbon crossover with expansion filter. Babypips."""
from strategies._common import nan, TREND, _xup, _xdn, ALL_CLASSES

META = {
    "id": "gmma_ribbon_crossover_compression",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "gmma_s, gmma_l",
    "long": "gmma_s crosses above gmma_l (short ribbon breaks above long ribbon)",
    "short": "gmma_s crosses below gmma_l (short ribbon breaks below long ribbon)",
    "desc": "Guppy Multiple MA ribbon crossover: short-term ribbon crosses long-term ribbon",
    "source": "https://www.babypips.com/learn/forex/guppy-multiple-moving-average",
}


def signal(ind, pos, htf=None):
    """GMMA ribbon crossover entry."""
    gs = ind["gmma_s"][pos]
    gs1 = ind["gmma_s"][pos - 1]
    gl = ind["gmma_l"][pos]
    gl1 = ind["gmma_l"][pos - 1]
    if nan(gs, gs1, gl, gl1):
        return None
    if _xup(gs, gs1, gl, gl1):
        return "long"
    if _xdn(gs, gs1, gl, gl1):
        return "short"
    return None
