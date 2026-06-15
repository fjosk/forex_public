#!/usr/bin/env python3
"""dual_moving_average_crossover_fast_slow -- Classic fast/slow EMA crossover stop-and-reverse system. Kaufman TSM Ch.5.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "dual_moving_average_crossover_fast_slow",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema20,ema50",
    "long": "EMA20 (fast) crosses above EMA50 (slow)",
    "short": "EMA20 crosses below EMA50",
    "desc": "Generic fast/slow MA crossover stop-and-reverse system; EMA20/EMA50 as representative periods",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.5 Techniques Using Two Trendlines",
}


def signal(ind, pos, htf=None):
    """EMA20 vs EMA50 crossover (generic fast/slow representative)."""
    if pos < 1:
        return None
    f = ind["ema20"][pos]
    f1 = ind["ema20"][pos - 1]
    s = ind["ema50"][pos]
    s1 = ind["ema50"][pos - 1]
    if nan(f, f1, s, s1):
        return None
    if f > s and f1 <= s1:
        return "long"
    if f < s and f1 >= s1:
        return "short"
    return None
