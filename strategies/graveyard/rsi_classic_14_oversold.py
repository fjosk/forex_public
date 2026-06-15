#!/usr/bin/env python3
"""rsi_classic_14_oversold -- RSI(14) crossover into OB/OS zones, 30/70 thresholds. Classic Nikhil-Adithyan.

Long when RSI crosses below 30 (enters oversold). Short when RSI crosses above 70 (enters overbought).
Requires a crossover, not just level touch, to prevent repeated signals on consecutive bars.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_classic_14_oversold",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "rsi",
    "long": "rsi crosses below 30 (rsi[pos-1] > 30 AND rsi[pos] < 30)",
    "short": "rsi crosses above 70 (rsi[pos-1] < 70 AND rsi[pos] > 70)",
    "desc": "Classic RSI 30/70 threshold crossover mean-reversion",
    "source": "web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """RSI crossover into oversold (long) or overbought (short) zone."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    if nan(r, r1):
        return None
    if r1 > 30 and r < 30:
        return "long"
    if r1 < 70 and r > 70:
        return "short"
    return None
