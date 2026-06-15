#!/usr/bin/env python3
"""kaufman_adaptive_moving_average_kama_cross_with_filter -- KAMA direction turn filtered by an ATR-scaled band; buy when KAMA rises more than 0.1 ATR. trade_your_way_to_financial_freedom."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "kaufman_adaptive_moving_average_kama_cross_with_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "kama, atr",
    "long": "KAMA rises by at least 0.1 ATR over one bar (turns up past filter)",
    "short": "KAMA falls by at least 0.1 ATR over one bar (turns down past filter)",
    "desc": "KAMA Cross with ATR filter: adaptive MA direction change exceeding 10% of ATR",
    "source": "book:trade_your_way_to_financial_freedom_mabroke_blogsp Ch 7-8",
}


def signal(ind, pos, htf=None):
    """KAMA turn filtered by 0.1 * ATR to suppress whipsaws."""
    if pos < 1:
        return None
    k = ind["kama"][pos]
    k1 = ind["kama"][pos - 1]
    a = ind["atr"][pos]
    if nan(k, k1, a):
        return None
    delta = k - k1
    band = 0.10 * a
    if delta > band:
        return "long"
    if delta < -band:
        return "short"
    return None
