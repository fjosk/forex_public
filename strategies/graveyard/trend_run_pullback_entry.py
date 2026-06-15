#!/usr/bin/env python3
"""trend_run_pullback_entry -- Theory of Runs: enter on a counter-trend close in trend direction. trading_systems_and_methods_kaufman_perry_j_kaufma.

Long-term trend: close > SMA200 (up) or close < SMA200 (down).
Long entry: trend up AND current close < prior close (down-close pullback day).
Short entry: trend down AND current close > prior close (up-close pullback day).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "trend_run_pullback_entry",
    "cadences": ["day"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "close,sma200",
    "long": "SMA200 trend up AND today close < yesterday close (pullback day -> buy)",
    "short": "SMA200 trend down AND today close > yesterday close (rally day -> sell)",
    "desc": "Theory of Runs pullback: enter long on down-close day in uptrend (Martingales variant entry)",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch22 pp569-571",
}


def signal(ind, pos, htf=None):
    """Enter on the first counter-trend close within the trend direction."""
    if pos < 1:
        return None
    c  = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    s  = ind["sma200"][pos]
    if nan(c, c1, s):
        return None
    trend_up = c > s
    trend_dn = c < s
    if trend_up and c < c1:
        return "long"
    if trend_dn and c > c1:
        return "short"
    return None
