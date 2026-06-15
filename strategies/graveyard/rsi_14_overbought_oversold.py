#!/usr/bin/env python3
"""rsi_14_overbought_oversold -- RSI(14) extreme OB/OS reversal with 20/80 FX thresholds.

Long when RSI < 20 (extreme oversold for FX); short when RSI > 80.
QuantConnect FX forum recommendation for tighter thresholds on forex pairs.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_14_overbought_oversold",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1d",
    "indicators": "rsi",
    "long": "rsi < 20 (extreme oversold, FX threshold)",
    "short": "rsi > 80 (extreme overbought, FX threshold)",
    "desc": "RSI 14 extreme OB/OS reversal using 20/80 FX-calibrated thresholds",
    "source": "web:https://www.quantconnect.com/forum/discussion/6908/",
}


def signal(ind, pos, htf=None):
    """RSI below 20 = long; RSI above 80 = short."""
    r = ind["rsi"][pos]
    if nan(r):
        return None
    if r < 20:
        return "long"
    if r > 80:
        return "short"
    return None
