#!/usr/bin/env python3
"""macd_above_zero_signal -- MACD above zero AND above signal line entry. freqtrade/berlinguyinca.

Long only when MACD is positive and above its signal line (momentum confirmed).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_above_zero_signal",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "macd, macd_sig",
    "long": "MACD > 0 AND MACD > macd_sig",
    "short": "MACD < 0 AND MACD < macd_sig",
    "desc": "MACD above zero and above signal line entry",
    "source": "https://github.com/freqtrade/freqtrade-strategies berlinguyinca/ASDTSRockwellTrading.py",
}


def signal(ind, pos, htf=None):
    """MACD above zero and above signal line."""
    m = ind["macd"][pos]
    s = ind["macd_sig"][pos]
    if nan(m, s):
        return None
    if m > 0 and m > s:
        return "long"
    if m < 0 and m < s:
        return "short"
    return None
