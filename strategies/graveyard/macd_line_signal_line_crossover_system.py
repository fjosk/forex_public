#!/usr/bin/env python3
"""macd_line_signal_line_crossover_system -- MACD line crosses signal line with explicit crossover detection (Elder, Trading for a Living).

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "macd_line_signal_line_crossover_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd, macd_sig",
    "long": "MACD(i) > Signal(i) AND MACD(i-1) <= Signal(i-1) -- crossover above",
    "short": "MACD(i) < Signal(i) AND MACD(i-1) >= Signal(i-1) -- crossover below",
    "desc": "Elder MACD line/signal line crossover system with explicit cross detection",
    "source": "Elder, Trading for a Living, Sec 26 MACD Trading Rules, p.129-130",
}


def signal(ind, pos, htf=None):
    """Explicit MACD/signal cross detection."""
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
