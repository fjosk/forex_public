#!/usr/bin/env python3
"""macd_fast_slow_line_crossover -- MACD fast line crosses above/below signal line (Appel MACD crossover). Person.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "macd_fast_slow_line_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd, macd_sig",
    "long": "MACD fast line crosses ABOVE signal line",
    "short": "MACD fast line crosses BELOW signal line",
    "desc": "Appel MACD fast/slow line crossover: long on golden cross, short on death cross",
    "source": "Person, A Complete Guide to Technical Trading Tactics, Ch.8 MACD, pp.142-143",
}


def signal(ind, pos, htf=None):
    """MACD line vs signal line crossover."""
    if pos < 1:
        return None
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    s = ind["macd_sig"][pos]
    s1 = ind["macd_sig"][pos - 1]
    if nan(m, m1, s, s1):
        return None
    if _xup(m, m1, s, s1):
        return "long"
    if _xdn(m, m1, s, s1):
        return "short"
    return None
