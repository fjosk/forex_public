#!/usr/bin/env python3
"""awesome_macd_ao -- Awesome MACD AO Crossover (AwesomeMacd freqtrade).
web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/AwesomeMacd.py
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "awesome_macd_ao",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "macd, ao",
    "long": "MACD > 0 AND AO > 0 AND AO[prev] < 0 (AO crosses above zero)",
    "short": "not implemented",
    "desc": "MACD above zero plus Awesome Oscillator zero-line crossover for trend continuation",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/AwesomeMacd.py",
}


def signal(ind, pos, htf=None):
    """Long when MACD > 0 and AO crosses above zero."""
    mc = ind["macd"][pos]
    ao = ind["ao"][pos]
    ao1 = ind["ao"][pos - 1]
    if nan(mc, ao, ao1):
        return None
    if mc > 0 and ao > 0 and ao1 < 0:
        return "long"
    return None
