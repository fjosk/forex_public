#!/usr/bin/env python3
"""rsi_ea_ob_os_zones -- RSI crossover into OB/OS zone EA (barabashkakvn MQL5 2019).

Long when RSI crosses below 30 (entering oversold). Short when RSI crosses above 70 (entering overbought).
Uses a bar-level crossover check to avoid multi-bar repeats.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_ea_ob_os_zones",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1d",
    "indicators": "rsi",
    "long": "rsi[pos-1] >= 30 AND rsi[pos] < 30 (crossing into oversold)",
    "short": "rsi[pos-1] <= 70 AND rsi[pos] > 70 (crossing into overbought)",
    "desc": "RSI OB/OS zone entry EA: enter on cross into extreme zone",
    "source": "web:https://www.mql5.com/en/code/23152",
}


def signal(ind, pos, htf=None):
    """RSI zone crossing: cross into oversold = long; cross into overbought = short."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    if nan(r, r1):
        return None
    if r1 >= 30 and r < 30:
        return "long"
    if r1 <= 70 and r > 70:
        return "short"
    return None
