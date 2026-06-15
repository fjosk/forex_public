#!/usr/bin/env python3
"""macd_cci_filter -- MACD above signal with CCI extreme filter. freqtrade/berlinguyinca.

MACD above signal line combined with CCI at extreme levels for entry confirmation.
Volume condition from source dropped (FX volume=0 always).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_cci_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "macd, macd_sig, cci",
    "long": "MACD > macd_sig AND CCI <= -100 (oversold dip in uptrend)",
    "short": "MACD < macd_sig AND CCI >= 100 (overbought spike in downtrend)",
    "desc": "MACD above signal with CCI extreme filter",
    "source": "https://github.com/freqtrade/freqtrade-strategies berlinguyinca/MACDStrategy.py",
}


def signal(ind, pos, htf=None):
    """MACD direction confirmed by CCI extreme."""
    m = ind["macd"][pos]
    s = ind["macd_sig"][pos]
    c = ind["cci"][pos]
    if nan(m, s, c):
        return None
    if m > s and c <= -100:
        return "long"
    if m < s and c >= 100:
        return "short"
    return None
