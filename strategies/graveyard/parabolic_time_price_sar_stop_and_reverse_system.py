#!/usr/bin/env python3
"""parabolic_time_price_sar_stop_and_reverse_system -- Wilder Parabolic SAR stop-and-reverse; enter on SAR direction flip. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_time_price_sar_stop_and_reverse_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "psar_dir",
    "long": "Price penetrates SAR upward: psar_dir flips to +1 (SAR now below price)",
    "short": "Price penetrates SAR downward: psar_dir flips to -1 (SAR now above price)",
    "desc": "Parabolic Time/Price SAR stop-and-reverse: always-in-market reversal on SAR flip",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma Ch 17 Wilder SAR",
}


def signal(ind, pos, htf=None):
    """Always-in-market reversal: enter on PSAR direction flip."""
    if pos < 1:
        return None
    d = ind["psar_dir"][pos]
    d1 = ind["psar_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d > 0 and d1 <= 0:
        return "long"
    if d < 0 and d1 >= 0:
        return "short"
    return None
