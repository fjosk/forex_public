#!/usr/bin/env python3
"""macd_rsi_bb_rising_up -- MACD positive + RSI momentum breakout + BB expanding. freqtrade/berlinguyinca.

Counterintuitive breakout: MACD positive and above signal, upper BB expanding, RSI14 > 65
(proxy for RSI7 > 70 per engine note). Long-only momentum breakout.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_rsi_bb_rising_up",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "macd, macd_sig, bb_up, rsi",
    "long": "MACD > 0 AND MACD > macd_sig AND bb_up rising AND RSI14 > 65",
    "short": "Not implemented (long-only breakout logic)",
    "desc": "MACD positive, BB expanding, RSI momentum breakout (long only)",
    "source": "https://github.com/freqtrade/freqtrade-strategies berlinguyinca/Simple.py",
}


def signal(ind, pos, htf=None):
    """MACD positive + rising upper BB + elevated RSI momentum breakout."""
    m = ind["macd"][pos]
    s = ind["macd_sig"][pos]
    bu = ind["bb_up"][pos]
    bu1 = ind["bb_up"][pos - 1]
    r = ind["rsi"][pos]
    if nan(m, s, bu, bu1, r):
        return None
    if m > 0 and m > s and bu > bu1 and r > 65:
        return "long"
    return None
