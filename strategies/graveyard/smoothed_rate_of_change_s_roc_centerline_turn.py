#!/usr/bin/env python3
"""smoothed_rate_of_change_s_roc_centerline_turn -- S-ROC (EMA13 then ROC21 of that EMA) turns up from below centerline = long; turns down from above = short. Elder.

tier1 momentum. Price/OHLC only. Uses sroc key (available in _INDICATORS.md).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "smoothed_rate_of_change_s_roc_centerline_turn",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "sroc",
    "long": "S-ROC below centerline (0) AND S-ROC turns up (S-ROC[i] > S-ROC[i-1])",
    "short": "S-ROC above centerline AND turns down (S-ROC[i] < S-ROC[i-1])",
    "desc": "Elder Smoothed ROC (EMA13 then ROC21) centerline turn: below-zero uptick = long; above-zero downtick = short",
    "source": "Elder, Trading for a Living, Sec 28 Smoothed Rate of Change, Fig 28-4, p.148-151",
}


def signal(ind, pos, htf=None):
    """S-ROC centerline turn signal."""
    if pos < 1:
        return None
    sr = ind["sroc"][pos]
    sr1 = ind["sroc"][pos - 1]
    if nan(sr, sr1):
        return None
    # Below centerline and ticking up
    if sr < 0 and sr > sr1:
        return "long"
    # Above centerline and ticking down
    if sr > 0 and sr < sr1:
        return "short"
    return None
