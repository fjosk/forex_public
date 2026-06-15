#!/usr/bin/env python3
"""parabolic_sar_trend_following -- Parabolic SAR direction flip with SMA200 trend filter.

Enter on psar_dir flip (+1 long, -1 short) only when aligned with the SMA200 trend.
The engine's ATR trailing stop handles the exit; the SAR itself signals the entry.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_trend_following",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "psar_dir, sma200",
    "long": "psar_dir flips to +1 and close > SMA200",
    "short": "psar_dir flips to -1 and close < SMA200",
    "desc": "Parabolic SAR direction flip with SMA200 trend alignment filter",
    "source": "web:https://forextraininggroup.com/parabolic-stop-and-reverse; Welles Wilder (1978)",
}


def signal(ind, pos, htf=None):
    """PSAR flip filtered by SMA200 trend direction."""
    pd0 = ind["psar_dir"][pos]
    pd1 = ind["psar_dir"][pos - 1]
    s200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(pd0, pd1, s200, c):
        return None
    if pd0 == 1 and pd1 == -1 and c > s200:
        return "long"
    if pd0 == -1 and pd1 == 1 and c < s200:
        return "short"
    return None
