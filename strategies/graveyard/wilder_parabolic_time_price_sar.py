#!/usr/bin/env python3
"""wilder_parabolic_time_price_sar -- Wilder Parabolic Time/Price SAR stop-and-reverse. trading_systems_and_methods_kaufman_perry_j_kaufma.

Always-in: long when PSAR direction flips from below to above (psar_dir changes from -1 to +1).
Short when PSAR direction flips from above to below.
psar_dir = +1 when SAR is below price (price above SAR, bullish), -1 when SAR above price (bearish).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "wilder_parabolic_time_price_sar",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "psar_dir,psar",
    "long": "PSAR direction flips to +1 (price crosses above parabolic SAR) -> stop-and-reverse long",
    "short": "PSAR direction flips to -1 (price crosses below SAR) -> stop-and-reverse short",
    "desc": "Wilder Parabolic Time/Price: always-in stop-and-reverse on PSAR direction flip",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch2 Parabolic Time/Price Wilder 1978",
}


def signal(ind, pos, htf=None):
    """PSAR direction flip -> stop-and-reverse."""
    if pos < 1:
        return None
    d  = ind["psar_dir"][pos]
    d1 = ind["psar_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d > 0 and d1 <= 0:
        return "long"
    if d < 0 and d1 >= 0:
        return "short"
    return None
