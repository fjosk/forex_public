#!/usr/bin/env python3
"""williams_percent_r_reversal -- Williams %R crossover from OB/OS back toward center. Nikhil-Adithyan.

Long when willr crosses above -80 from extreme oversold (recovery signal).
Short when willr crosses below -20 from extreme overbought.
Scale: willr ranges -100 (oversold) to 0 (overbought) -- inverted vs RSI convention.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "williams_percent_r_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1d",
    "indicators": "willr",
    "long": "willr crosses above -80 (recovery from oversold)",
    "short": "willr crosses below -20 (reversal from overbought)",
    "desc": "Williams %R crossover recovery: long on OS exit, short on OB exit",
    "source": "web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """Williams %R crosses back above -80 (long) or below -20 (short)."""
    wr = ind["willr"][pos]
    wr1 = ind["willr"][pos - 1]
    if nan(wr, wr1):
        return None
    if wr > -80 and wr1 <= -80:
        return "long"
    if wr < -20 and wr1 >= -20:
        return "short"
    return None
