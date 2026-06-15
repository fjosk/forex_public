#!/usr/bin/env python3
"""rsi_50_ema200_momentum -- EMA200 trend bias + RSI(14) crosses 50. BabyPips / retail forex standard."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "rsi_50_ema200_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema200, rsi",
    "long": "close > ema200 AND rsi crosses above 50",
    "short": "close < ema200 AND rsi crosses below 50",
    "desc": "EMA200 trend filter + RSI 50 crossover momentum entry",
    "source": "web:https://www.babypips.com/learn/forex/moving-average-crossover-trading",
}


def signal(ind, pos, htf=None):
    """EMA200 trend direction + RSI 50 crossover."""
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    rs = ind["rsi"][pos]
    rsp = ind["rsi"][pos - 1]
    if nan(c, e200, rs, rsp):
        return None
    above = c > e200
    rsi_up = rs > 50 and rsp <= 50
    rsi_dn = rs < 50 and rsp >= 50
    if above and rsi_up:
        return "long"
    if not above and rsi_dn:
        return "short"
    return None
