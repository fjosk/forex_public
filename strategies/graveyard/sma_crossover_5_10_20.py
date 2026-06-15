#!/usr/bin/env python3
"""sma_crossover_5_10_20 -- Three SMA perfect-order crossover (5/10/20). web:trendspider.com.

close_sma5 crosses sma10 with sma10 > sma20 for longs (reverse for shorts).
All three in perfect stack when entry fires. No volume dependency.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "sma_crossover_5_10_20",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close_sma5, sma10, sma20",
    "long": "close_sma5 crosses above sma10 AND sma10 > sma20",
    "short": "close_sma5 crosses below sma10 AND sma10 < sma20",
    "desc": "Three SMA (5/10/20) perfect-order crossover",
    "source": "web:https://trendspider.com/learning-center/moving-average-crossover-strategies/",
}


def signal(ind, pos, htf=None):
    """Fast SMA crosses medium SMA while all three in perfect order."""
    s5, s5p = ind["close_sma5"][pos], ind["close_sma5"][pos - 1]
    s10, s10p = ind["sma10"][pos], ind["sma10"][pos - 1]
    s20 = ind["sma20"][pos]
    if nan(s5, s5p, s10, s10p, s20):
        return None
    if _xup(s5, s5p, s10, s10p) and s10 > s20:
        return "long"
    if _xdn(s5, s5p, s10, s10p) and s10 < s20:
        return "short"
    return None
