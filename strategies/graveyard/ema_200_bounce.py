#!/usr/bin/env python3
"""ema_200_bounce -- EMA200 pullback bounce with reversal bar confirmation. web:https://www.forexfactory.com/thread/405237-100ema-200ema-pullback-system-using-mtfa"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_200_bounce",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema200, atr, close, open, high, low",
    "long": "price sustained above ema200, low touches ema200, bullish reversal candle",
    "short": "price sustained below ema200, high touches ema200, bearish reversal candle",
    "desc": "EMA200 pullback bounce strategy with reversal bar confirmation",
    "source": "web:https://www.forexfactory.com/thread/405237-100ema-200ema-pullback-system-using-mtfa",
}


def signal(ind, pos, htf=None):
    """Price bounces off EMA200 in established trend."""
    c = ind["close"][pos]
    c5 = ind["close"][pos - 5]
    o = ind["open"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    e200 = ind["ema200"][pos]
    atr = ind["atr"][pos]
    if nan(c, c5, o, hi, lo, e200, atr):
        return None
    trend_up = c5 > e200 and c > e200
    trend_dn = c5 < e200 and c < e200
    touched_bull = lo <= e200 and c > e200
    touched_bear = hi >= e200 and c < e200
    bull_rev = c > o and c > ind["close"][pos - 1]
    bear_rev = c < o and c < ind["close"][pos - 1]
    if trend_up and touched_bull and bull_rev:
        return "long"
    if trend_dn and touched_bear and bear_rev:
        return "short"
    return None
