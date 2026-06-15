#!/usr/bin/env python3
"""macd_bollinger_dual_confirm -- MACD + BB Dual Confirmation. zeta-zetra blog.

Enter only when MACD crossover and BB band breakout agree simultaneously.
Variant of macd_bollinger_combined_breakout with same logic; kept as separate entry per spec.
"""
from strategies._common import nan, _xup, _xdn, BREAK, ALL_CLASSES

META = {
    "id": "macd_bollinger_dual_confirm",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "macd, macd_sig, bb_up, bb_lo, close",
    "long": "macd crosses above signal (macd[-1]<sig[-1], macd[0]>=sig[0]) AND close > bb_up",
    "short": "macd crosses below signal (macd[-1]>sig[-1], macd[0]<=sig[0]) AND close < bb_lo",
    "desc": "MACD + Bollinger Bands dual confirmation: both breakout signals required simultaneously",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/blogs/bollinger_macd.html",
}


def signal(ind, pos, htf=None):
    """MACD + BB dual confirm breakout."""
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    ms = ind["macd_sig"][pos]
    ms1 = ind["macd_sig"][pos - 1]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    c = ind["close"][pos]
    if nan(m, m1, ms, ms1, bb_up, bb_lo, c):
        return None
    macd_bull = m1 < ms1 and m >= ms
    macd_bear = m1 > ms1 and m <= ms
    if macd_bull and c > bb_up:
        return "long"
    if macd_bear and c < bb_lo:
        return "short"
    return None
