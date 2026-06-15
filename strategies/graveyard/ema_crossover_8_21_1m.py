#!/usr/bin/env python3
"""ema_crossover_8_21_1m -- EMA8/21 cross with EMA50 trend filter and candle confirmation. web:fxnx.com."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "ema_crossover_8_21_1m",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "ema8, ema21, ema50",
    "long": "EMA8 crosses above EMA21 AND close > ema50 AND bullish candle above both EMAs",
    "short": "EMA8 crosses below EMA21 AND close < ema50 AND bearish candle below both EMAs",
    "desc": "EMA8/21 crossover scalp with EMA50 trend filter and candle confirmation",
    "source": "web:https://fxnx.com/en/blog/ema-crossover-strategy-1-minute-scalping-blueprint",
}


def signal(ind, pos, htf=None):
    """Fast EMA cross with trend filter and confirming candle body requirement."""
    e8 = ind["ema8"][pos]
    e8p = ind["ema8"][pos - 1]
    e21 = ind["ema21"][pos]
    e21p = ind["ema21"][pos - 1]
    e50 = ind["ema50"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    if nan(e8, e8p, e21, e21p, e50, c, o):
        return None
    if _xup(e8, e8p, e21, e21p) and c > o and c > max(e8, e21) and c > e50:
        return "long"
    if _xdn(e8, e8p, e21, e21p) and c < o and c < min(e8, e21) and c < e50:
        return "short"
    return None
