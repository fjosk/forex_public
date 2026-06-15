#!/usr/bin/env python3
"""moving_average_crossover_reversal_two_ma -- Fast MA crosses slow MA stop-and-reverse; SMA10 vs SMA50. trade_your_way_to_financial_freedom."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "moving_average_crossover_reversal_two_ma",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma10, sma50",
    "long": "SMA10 crosses above SMA50 (fast MA over slow MA)",
    "short": "SMA10 crosses below SMA50 (fast MA under slow MA)",
    "desc": "Two-MA crossover reversal: fast crosses slow for always-in-market trend following",
    "source": "book:trade_your_way_to_financial_freedom_mabroke_blogsp Ch 9",
}


def signal(ind, pos, htf=None):
    """Fast SMA crosses slow SMA; reverse on opposite cross."""
    if pos < 1:
        return None
    fast = ind["sma10"][pos]
    fast1 = ind["sma10"][pos - 1]
    slow = ind["sma50"][pos]
    slow1 = ind["sma50"][pos - 1]
    if nan(fast, fast1, slow, slow1):
        return None
    if _xup(fast, fast1, slow, slow1):
        return "long"
    if _xdn(fast, fast1, slow, slow1):
        return "short"
    return None
