#!/usr/bin/env python3
"""macd_bollinger_combined_breakout -- MACD + BB Combined Breakout. zeta-zetra blogs.

MACD crosses above signal AND close > bb_up = high-conviction long breakout.
MACD crosses below signal AND close < bb_lo = strong short breakout.
"""
from strategies._common import nan, _xup, _xdn, BREAK, ALL_CLASSES

META = {
    "id": "macd_bollinger_combined_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "macd, macd_sig, bb_up, bb_lo, close",
    "long": "macd crosses above signal AND close > bb_up (MACD bullish + BB upper breakout)",
    "short": "macd crosses below signal AND close < bb_lo (MACD bearish + BB lower breakout)",
    "desc": "MACD crossover confluent with Bollinger Band breakout for high-conviction entry",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/blogs/bollinger_macd.html",
}


def signal(ind, pos, htf=None):
    """MACD crossover + BB breakout simultaneous entry."""
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    ms = ind["macd_sig"][pos]
    ms1 = ind["macd_sig"][pos - 1]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    c = ind["close"][pos]
    if nan(m, m1, ms, ms1, bb_up, bb_lo, c):
        return None
    if _xup(m, m1, ms, ms1) and c > bb_up:
        return "long"
    if _xdn(m, m1, ms, ms1) and c < bb_lo:
        return "short"
    return None
