#!/usr/bin/env python3
"""kaufman_adaptive_moving_average_kama_trend -- KAMA slope direction (up/down) as trend signal. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "kaufman_adaptive_moving_average_kama_trend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "kama",
    "long": "KAMA trendline turns UP (current KAMA > prior KAMA)",
    "short": "KAMA trendline turns DOWN (current KAMA < prior KAMA)",
    "desc": "KAMA trend direction: trade the sign of the adaptive MA slope",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma Ch 17",
}


def signal(ind, pos, htf=None):
    """Long when KAMA slope turns up, short when turns down."""
    if pos < 1:
        return None
    k = ind["kama"][pos]
    k1 = ind["kama"][pos - 1]
    if nan(k, k1):
        return None
    if k > k1:
        return "long"
    if k < k1:
        return "short"
    return None
