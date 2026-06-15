#!/usr/bin/env python3
"""macd_rsi_combined_backtrader -- MACD + RSI Combined (Backtrader). sammeowww/backtrader_strategy.

MACD crosses above signal while MACD < 0 AND RSI < 50 = early oversold recovery long.
Symmetric short: MACD crosses below signal while MACD > 0 AND RSI > 50.
Standard MACD(12/26/9) and RSI(14) used (source uses 8/21/6 and RSI13; approximation noted).
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "macd_rsi_combined_backtrader",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "macd, macd_sig, rsi",
    "long": "macd crosses above signal AND macd < 0 AND rsi < 50 (early recovery from oversold)",
    "short": "macd crosses below signal AND macd > 0 AND rsi > 50 (early rollover from overbought)",
    "desc": "MACD below-zero crossover with RSI < 50 filter (Backtrader community strategy)",
    "source": "web:https://github.com/sammeowww/backtrader_strategy/blob/main/macd_rsi.py",
}


def signal(ind, pos, htf=None):
    """MACD crossover below zero with RSI directional filter."""
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    ms = ind["macd_sig"][pos]
    ms1 = ind["macd_sig"][pos - 1]
    r = ind["rsi"][pos]
    if nan(m, m1, ms, ms1, r):
        return None
    if _xup(m, m1, ms, ms1) and m < 0 and r < 50:
        return "long"
    if _xdn(m, m1, ms, ms1) and m > 0 and r > 50:
        return "short"
    return None
