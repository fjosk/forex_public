#!/usr/bin/env python3
"""macd_line_crossover_entry -- MACD fast line crosses above/below signal line (Elder, Come Into My Trading Room). Entry-only; exit handled by engine ATR envelope.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "macd_line_crossover_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd, macd_sig",
    "long": "Fast MACD line crosses ABOVE slow signal line",
    "short": "Fast MACD line crosses BELOW slow signal line",
    "desc": "Elder MACD crossover entry: golden cross long, death cross short; engine ATR exit",
    "source": "Elder, Come Into My Trading Room, Ch5 MACD-Histogram / MACD Lines, Fig 5.8, p.102-104",
}


def signal(ind, pos, htf=None):
    """MACD line vs signal line crossover entry."""
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
