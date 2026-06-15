#!/usr/bin/env python3
"""rsi_overbought_oversold_ea -- RSI crossover OB/OS EA (DXerof MQL4 2015).

Buy when RSI just enters oversold (crosses below 30). Sell when RSI just enters overbought
(crosses above 70). Entry on bar close after the crossing bar.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_overbought_oversold_ea",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "rsi",
    "long": "rsi[pos] < 30 AND rsi[pos-1] >= 30 (just entered oversold)",
    "short": "rsi[pos] > 70 AND rsi[pos-1] <= 70 (just entered overbought)",
    "desc": "RSI OB/OS zone entry EA: long on oversold cross, short on overbought cross",
    "source": "web:https://www.mql5.com/en/code/13625",
}


def signal(ind, pos, htf=None):
    """RSI crossover into OB/OS zone."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    if nan(r, r1):
        return None
    if r < 30 and r1 >= 30:
        return "long"
    if r > 70 and r1 <= 70:
        return "short"
    return None
