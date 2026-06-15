#!/usr/bin/env python3
"""parabolic_sar_trend_follow -- Classic PSAR below/above price direction. je-suis-tm/quant-trading.

Long when SAR is below price (bullish mode), short when SAR is above price (bearish mode).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_trend_follow",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "psar, psar_dir",
    "long": "PSAR below close (psar_dir == 1)",
    "short": "PSAR above close (psar_dir == -1)",
    "desc": "Parabolic SAR trend follow: long when SAR trails below price",
    "source": "https://github.com/je-suis-tm/quant-trading Parabolic SAR backtest.py",
}


def signal(ind, pos, htf=None):
    """PSAR direction signal: 1=bull, -1=bear."""
    d = ind["psar_dir"][pos]
    d1 = ind["psar_dir"][pos - 1]
    if nan(d, d1):
        return None
    # Only signal on direction flips to avoid re-entry in same trend
    if d == 1 and d1 != 1:
        return "long"
    if d == -1 and d1 != -1:
        return "short"
    return None
