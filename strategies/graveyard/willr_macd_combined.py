#!/usr/bin/env python3
"""willr_macd_combined -- Williams %R OB/OS levels with MACD direction. Nikhil-Adithyan W%R_MACD.py.

Williams %R in oversold (<-80) or overbought (>-20) territory combined with MACD direction.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "willr_macd_combined",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h",
    "indicators": "willr, macd, macd_sig",
    "long": "Williams %R < -80 (oversold) AND MACD > macd_sig (bullish)",
    "short": "Williams %R > -20 (overbought) AND MACD < macd_sig (bearish)",
    "desc": "Williams %R oversold/overbought levels with MACD direction confirmation",
    "source": "https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python W%R_MACD.py",
}


def signal(ind, pos, htf=None):
    """Williams %R OB/OS with MACD direction."""
    w = ind["willr"][pos]
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    if nan(w, m, ms):
        return None
    if w < -80 and m > ms:
        return "long"
    if w > -20 and m < ms:
        return "short"
    return None
