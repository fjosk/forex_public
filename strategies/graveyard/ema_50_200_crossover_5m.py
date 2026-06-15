#!/usr/bin/env python3
"""ema_50_200_crossover_5m -- EMA50/200 golden/death cross with candle confirmation. web:tradersunion.com."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "ema_50_200_crossover_5m",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "5m",
    "indicators": "ema50, ema200",
    "long": "EMA50 crosses above EMA200 with bullish confirming candle",
    "short": "EMA50 crosses below EMA200 with bearish confirming candle",
    "desc": "EMA50/200 golden/death cross momentum entry scalp",
    "source": "web:https://tradersunion.com/interesting-articles/what-is-scalping/1-minute-scalping-strategy/",
}


def signal(ind, pos, htf=None):
    """EMA50/200 cross with same-bar candle confirmation."""
    e50 = ind["ema50"][pos]
    e50p = ind["ema50"][pos - 1]
    e200 = ind["ema200"][pos]
    e200p = ind["ema200"][pos - 1]
    c = ind["close"][pos]
    o = ind["open"][pos]
    if nan(e50, e50p, e200, e200p, c, o):
        return None
    if _xup(e50, e50p, e200, e200p) and c > o:
        return "long"
    if _xdn(e50, e50p, e200, e200p) and c < o:
        return "short"
    return None
