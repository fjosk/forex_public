#!/usr/bin/env python3
"""macd_zero_line_gated_signal_line_crossover -- MACD/signal crossover gated by MACD side of zero: cross-up while MACD<0 = long; cross-down while MACD>0 = short. Currency Trading for Dummies.

tier1 momentum, FX-native. Price/OHLC only.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "macd_zero_line_gated_signal_line_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd, macd_sig",
    "long": "MACD crosses ABOVE signal line WHILE MACD < 0 (oversold momentum reversal)",
    "short": "MACD crosses BELOW signal line WHILE MACD > 0 (overbought momentum reversal)",
    "desc": "MACD/signal cross gated by zero-line position: cross-up from below zero = long; cross-down from above zero = short",
    "source": "Currency Trading for Dummies, Ch.11 Momentum oscillators MACD; Ch.12 divergence example",
}


def signal(ind, pos, htf=None):
    """MACD/signal crossover filtered by MACD position relative to zero."""
    if pos < 1:
        return None
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    s = ind["macd_sig"][pos]
    s1 = ind["macd_sig"][pos - 1]
    if nan(m, m1, s, s1):
        return None
    if _xup(m, m1, s, s1) and m < 0:
        return "long"
    if _xdn(m, m1, s, s1) and m > 0:
        return "short"
    return None
