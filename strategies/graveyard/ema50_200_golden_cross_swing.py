#!/usr/bin/env python3
"""ema50_200_golden_cross_swing -- EMA50/200 golden/death cross with pullback entry. web:https://www.tradingwithrayner.com/golden-cross-trading-strategy/"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema50_200_golden_cross_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "ema50, ema200, atr, close, high, low",
    "long": "ema50 > ema200 (golden cross in effect), price pulls back to touch ema50, bullish close",
    "short": "ema50 < ema200 (death cross), price rallies to ema50, bearish candle",
    "desc": "EMA50/200 golden cross swing -- buy pullbacks to EMA50 in golden cross regime",
    "source": "web:https://www.tradingwithrayner.com/golden-cross-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Pullback to EMA50 in EMA50/200 golden-cross regime."""
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    if nan(e50, e200, lo, hi, c, o):
        return None
    golden = e50 > e200
    death = e50 < e200
    # price touched ema50 zone (low pierced, closed above for long; high pierced, closed below for short)
    touch_bull = lo < e50 * 1.002 and c > e50 * 0.998
    touch_bear = hi > e50 * 0.998 and c < e50 * 1.002
    bull_candle = c > o
    bear_candle = c < o
    if golden and touch_bull and bull_candle:
        return "long"
    if death and touch_bear and bear_candle:
        return "short"
    return None
