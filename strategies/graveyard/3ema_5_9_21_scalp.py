#!/usr/bin/env python3
"""3ema_5_9_21_scalp -- Triple EMA 5/9/21 stack + pullback to EMA9 scalp. web:opofinance.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "3ema_5_9_21_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "15m",
    "indicators": "ema5, ema9, ema21, close, open",
    "long": "EMA5 > EMA9 > EMA21 (bull stack), close near EMA9, bullish candle",
    "short": "EMA5 < EMA9 < EMA21 (bear stack), close near EMA9, bearish candle",
    "desc": "Triple EMA 5/9/21 pullback scalp: stack alignment and candle at EMA9",
    "source": "web:https://blog.opofinance.com/en/3-ema-scalping-strategy/",
}


def signal(ind, pos, htf=None):
    """EMA5/9/21 stack pullback scalp."""
    e5, e9, e21 = ind["ema5"][pos], ind["ema9"][pos], ind["ema21"][pos]
    c, o = ind["close"][pos], ind["open"][pos]
    atr = ind["atr"][pos]
    if nan(e5, e9, e21, c, o, atr):
        return None
    if atr <= 0:
        return None
    # Near EMA9: within 1 ATR (covers different pair pip values)
    near_9 = abs(c - e9) < atr
    body = abs(c - o)
    bar_rng = ind["high"][pos] - ind["low"][pos]
    bull_body = c > o and (body > 0.4 * bar_rng if bar_rng > 0 else False)
    bear_body = c < o and (body > 0.4 * bar_rng if bar_rng > 0 else False)
    if e5 > e9 and e9 > e21 and near_9 and bull_body:
        return "long"
    if e5 < e9 and e9 < e21 and near_9 and bear_body:
        return "short"
    return None
