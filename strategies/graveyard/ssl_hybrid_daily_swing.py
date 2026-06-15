#!/usr/bin/env python3
"""ssl_hybrid_daily_swing -- SSL Hybrid flip with QQE momentum and SMA200 filter. web:theforexgeek.com.

ssl_hlv direction flip as the primary trend-change signal. Optional filters: qqe_line
positive/negative for momentum, sma200 side for macro bias.
No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ssl_hybrid_daily_swing",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "ssl_hlv, qqe_line, sma200",
    "long": "ssl_hlv flips to +1 AND close > sma200 AND qqe_line > 0",
    "short": "ssl_hlv flips to -1 AND close < sma200 AND qqe_line < 0",
    "desc": "SSL Hybrid daily flip filtered by SMA200 and QQE line sign",
    "source": "web:https://theforexgeek.com/ssl-hybrid-indicator-tradingview/",
}


def signal(ind, pos, htf=None):
    """SSL hlv flip with SMA200 and QQE momentum filters."""
    hlv = ind["ssl_hlv"][pos]
    hlvp = ind["ssl_hlv"][pos - 1]
    c = ind["close"][pos]
    sma = ind["sma200"][pos]
    qqe = ind["qqe_line"][pos]
    if nan(hlv, hlvp, c, sma, qqe):
        return None
    if hlv == 1 and hlvp == -1 and c > sma and qqe > 0:
        return "long"
    if hlv == -1 and hlvp == 1 and c < sma and qqe < 0:
        return "short"
    return None
