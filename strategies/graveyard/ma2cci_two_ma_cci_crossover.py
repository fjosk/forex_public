#!/usr/bin/env python3
"""ma2cci_two_ma_cci_crossover -- MA2CCI Two MAs + CCI Crossover EA. Orchard Forex/Andrea Forex.

Fast MA (ema9) crosses above slow MA (ema21) AND CCI crosses above zero = long.
Reverse for short. Both the MA crossover and CCI zero-cross must fire on the same bar.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ma2cci_two_ma_cci_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema9, ema21, cci",
    "long": "ema9 crosses above ema21 AND cci crosses above zero",
    "short": "ema9 crosses below ema21 AND cci crosses below zero",
    "desc": "EMA9/EMA21 crossover confirmed by simultaneous CCI zero-line cross",
    "source": "web:https://orchardforex.com/write-an-expert-for-mt4-or-mt5-using-cci-and-2-moving-averages/",
}


def signal(ind, pos, htf=None):
    """EMA crossover + CCI zero-cross dual confirmation."""
    e9 = ind["ema9"][pos]
    e91 = ind["ema9"][pos - 1]
    e21 = ind["ema21"][pos]
    e211 = ind["ema21"][pos - 1]
    cc = ind["cci"][pos]
    cc1 = ind["cci"][pos - 1]
    if nan(e9, e91, e21, e211, cc, cc1):
        return None
    if _xup(e9, e91, e21, e211) and _xup(cc, cc1, 0.0, 0.0):
        return "long"
    if _xdn(e9, e91, e21, e211) and _xdn(cc, cc1, 0.0, 0.0):
        return "short"
    return None
