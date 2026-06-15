#!/usr/bin/env python3
"""freqtrade_macd_cci -- Freqtrade MACD + CCI Entry. berlinguyinca/MACDStrategy.py.

MACD line crosses above signal AND CCI <= -50 = long. Long-only in source.
Symmetric short added for FX: MACD crosses below signal AND CCI >= 100.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "freqtrade_macd_cci",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "5m",
    "indicators": "macd, macd_sig, cci",
    "long": "macd crosses above macd_sig AND cci <= -50",
    "short": "macd crosses below macd_sig AND cci >= 100",
    "desc": "MACD crossover confirmed by CCI oversold/overbought threshold",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/MACDStrategy.py",
}


def signal(ind, pos, htf=None):
    """MACD crossover with CCI confirmation."""
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    ms = ind["macd_sig"][pos]
    ms1 = ind["macd_sig"][pos - 1]
    cc = ind["cci"][pos]
    if nan(m, m1, ms, ms1, cc):
        return None
    if _xup(m, m1, ms, ms1) and cc <= -50:
        return "long"
    if _xdn(m, m1, ms, ms1) and cc >= 100:
        return "short"
    return None
