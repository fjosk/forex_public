#!/usr/bin/env python3
"""kaufman_efficiency_ratio_adaptive_trend_filter_kama -- Price vs KAMA trend with Efficiency Ratio gate; only trade when ER >= 0.6 (clean directional move). trade_your_way_to_financial_freedom."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "kaufman_efficiency_ratio_adaptive_trend_filter_kama",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "kama, er10, close",
    "long": "Price above KAMA AND Efficiency Ratio >= 0.6 (clean uptrend)",
    "short": "Price below KAMA AND Efficiency Ratio >= 0.6 (clean downtrend)",
    "desc": "KAMA trend with ER gate: only enter when market is trending cleanly (ER >= 0.6)",
    "source": "book:trade_your_way_to_financial_freedom_mabroke_blogsp Ch 7",
}

ER_THRESHOLD = 0.6


def signal(ind, pos, htf=None):
    """Price vs KAMA with Efficiency Ratio threshold gate."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    k = ind["kama"][pos]
    er = ind["er10"][pos]
    if nan(c, k, er):
        return None
    if er < ER_THRESHOLD:
        return None
    if c > k:
        return "long"
    if c < k:
        return "short"
    return None
