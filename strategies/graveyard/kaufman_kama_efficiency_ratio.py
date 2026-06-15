#!/usr/bin/env python3
"""kaufman_kama_efficiency_ratio -- KAMA vs EMA200 trend filter + KAMA slope. machinelearning-basics/Kaufman."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "kaufman_kama_efficiency_ratio",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "kama, ema200, close",
    "long": "kama > ema200 (KAMA above long-term trend) AND kama rising",
    "short": "kama < ema200 (KAMA below long-term trend) AND kama falling",
    "desc": "Kaufman KAMA dual crossover: KAMA vs EMA200 trend filter with KAMA slope confirmation",
    "source": "machinelearning-basics.com KAMA Python tutorial; Perry Kaufman Smarter Trading (1995)",
}


def signal(ind, pos, htf=None):
    """KAMA above/below EMA200 with KAMA slope as trend confirmation."""
    k = ind["kama"][pos]
    k1 = ind["kama"][pos - 1]
    e200 = ind["ema200"][pos]
    if nan(k, k1, e200):
        return None
    kama_rising = k > k1
    kama_falling = k < k1
    if k > e200 and kama_rising:
        return "long"
    if k < e200 and kama_falling:
        return "short"
    return None
