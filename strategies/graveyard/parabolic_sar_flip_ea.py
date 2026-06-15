#!/usr/bin/env python3
"""parabolic_sar_flip_ea -- Always-in-market PSAR flip reversal EA. EarnForex PSAR EA."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_flip_ea",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "psar_dir",
    "long": "psar_dir[pos-1] < 0 AND psar_dir[pos] > 0 (SAR flipped from above to below price)",
    "short": "psar_dir[pos-1] > 0 AND psar_dir[pos] < 0 (SAR flipped from below to above price)",
    "desc": "Always-in-market PSAR flip EA: reverse on every direction change",
    "source": "EarnForex PSAR EA (MQL4); earnforex.com/metatrader-expert-advisors/psar/",
}


def signal(ind, pos, htf=None):
    """Long on bullish PSAR flip; short on bearish PSAR flip."""
    d = ind["psar_dir"][pos]
    d1 = ind["psar_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d1 < 0 and d > 0:
        return "long"
    if d1 > 0 and d < 0:
        return "short"
    return None
