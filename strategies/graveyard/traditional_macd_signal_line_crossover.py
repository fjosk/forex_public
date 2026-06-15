#!/usr/bin/env python3
"""traditional_macd_signal_line_crossover -- MACD has been declining then crosses above signal = long; rising then crosses below signal = short. Naked Forex.

tier1 momentum, FX-native. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "traditional_macd_signal_line_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd, macd_sig",
    "long": "MACD crosses above signal line after MACD was below zero (declining context)",
    "short": "MACD crosses below signal line after MACD was above zero (rising context)",
    "desc": "Traditional MACD crossover with zero-side context: buy after depressed MACD crosses up; sell after elevated MACD crosses down",
    "source": "Naked Forex, Ch.2 Avoiding a Trading Tragedy, p.12-14, Figures 2.3-2.4",
}


def signal(ind, pos, htf=None):
    """MACD/signal cross gated by MACD having been on its respective side of zero."""
    if pos < 1:
        return None
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    s = ind["macd_sig"][pos]
    s1 = ind["macd_sig"][pos - 1]
    if nan(m, m1, s, s1):
        return None
    # Long: cross up AND MACD was below zero context (depressed/declining)
    if _xup(m, m1, s, s1) and m1 < 0:
        return "long"
    # Short: cross down AND MACD was above zero context (elevated/rising)
    if _xdn(m, m1, s, s1) and m1 > 0:
        return "short"
    return None
