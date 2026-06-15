#!/usr/bin/env python3
"""ema_10_40_crossover_davey -- EMA 10/40 Crossover (Exponentially Better, Kevin Davey).
web:https://zeta-zetra.github.io/docs-forex-strategies-python/books/exponentially_better.html
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema_10_40_crossover_davey",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "ema9, ema50",
    "long": "ema9 (proxy ema10) crosses above ema50 (proxy ema40)",
    "short": "ema9 crosses below ema50",
    "desc": "Kevin Davey EMA 10/40 crossover; approximated with ema9/ema50 (closest available periods)",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/books/exponentially_better.html",
}


def signal(ind, pos, htf=None):
    """EMA9/EMA50 crossover (approximating EMA10/EMA40 from Kevin Davey)."""
    e9 = ind["ema9"][pos]
    e50 = ind["ema50"][pos]
    e9_1 = ind["ema9"][pos - 1]
    e50_1 = ind["ema50"][pos - 1]
    if nan(e9, e50, e9_1, e50_1):
        return None
    if _xup(e9, e9_1, e50, e50_1):
        return "long"
    if _xdn(e9, e9_1, e50, e50_1):
        return "short"
    return None
