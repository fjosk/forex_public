#!/usr/bin/env python3
"""macd_signal_cross -- MACD line crosses signal line with ADX trend filter. EarnForex."""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "macd_signal_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h/4h",
    "indicators": "macd, macd_sig, adx",
    "long": "MACD crosses above signal line AND ADX > 20",
    "short": "MACD crosses below signal line AND ADX > 20",
    "desc": "MACD signal-line crossover with ADX trend-strength gate",
    "source": "web:https://www.earnforex.com/forex-strategy/moving-average-cross-strategy/",
}


def signal(ind, pos, htf=None):
    """MACD vs signal-line cross gated by ADX > 20."""
    if pos < 1:
        return None
    m0 = ind["macd"][pos]
    ms0 = ind["macd_sig"][pos]
    m1 = ind["macd"][pos - 1]
    ms1 = ind["macd_sig"][pos - 1]
    adx = ind["adx"][pos]
    if nan(m0, ms0, m1, ms1, adx):
        return None

    if adx > 20 and _xup(m0, m1, ms0, ms1):
        return "long"
    if adx > 20 and _xdn(m0, m1, ms0, ms1):
        return "short"

    return None
