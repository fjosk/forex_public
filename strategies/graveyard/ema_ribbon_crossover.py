#!/usr/bin/env python3
"""ema_ribbon_crossover -- Multi-EMA ribbon crossover with ADX strength filter. web:stockpathshala."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ema_ribbon_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "ema8, ema13, ema21, ema50, ema200, adx",
    "long": "fast ribbon (ema8/13/21) fully above slow ribbon (ema50/200), first crossover bar, adx > 20",
    "short": "fast ribbon fully below slow ribbon, first crossover bar, adx > 20",
    "desc": "EMA ribbon crossover: fast group crosses above/below slow group with ADX trend gate",
    "source": "web:https://stockpathshala.com/ema-crossover/",
}

_ADX_MIN = 20.0


def signal(ind, pos, htf=None):
    """EMA ribbon crossover with ADX filter."""
    e8 = ind["ema8"][pos]
    e13 = ind["ema13"][pos]
    e21 = ind["ema21"][pos]
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    adx = ind["adx"][pos]
    e8_1 = ind["ema8"][pos - 1]
    e13_1 = ind["ema13"][pos - 1]
    e21_1 = ind["ema21"][pos - 1]
    e50_1 = ind["ema50"][pos - 1]
    e200_1 = ind["ema200"][pos - 1]
    if nan(e8, e13, e21, e50, e200, adx, e8_1, e13_1, e21_1, e50_1, e200_1):
        return None
    if adx < _ADX_MIN:
        return None
    fast_min = min(e8, e13, e21)
    fast_max = max(e8, e13, e21)
    slow_max = max(e50, e200)
    slow_min = min(e50, e200)
    fast_min1 = min(e8_1, e13_1, e21_1)
    fast_max1 = max(e8_1, e13_1, e21_1)
    slow_max1 = max(e50_1, e200_1)
    slow_min1 = min(e50_1, e200_1)
    # Ribbon now fully above slow: fast_min > slow_max (cross from below)
    bull_now = fast_min > slow_max
    bull_prev = fast_min1 > slow_max1
    # Ribbon now fully below slow: fast_max < slow_min
    bear_now = fast_max < slow_min
    bear_prev = fast_max1 < slow_min1
    # Expanding fast group
    expanding_up = e8 > e13 > e21
    expanding_dn = e8 < e13 < e21
    if bull_now and not bull_prev and expanding_up:
        return "long"
    if bear_now and not bear_prev and expanding_dn:
        return "short"
    return None
