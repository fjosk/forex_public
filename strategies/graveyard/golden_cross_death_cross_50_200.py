#!/usr/bin/env python3
"""golden_cross_death_cross_50_200 -- SMA50/200 cross then pullback entry. web:https://pippenguin.net/forex/learn-forex/golden-cross-trading-strategy/"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "golden_cross_death_cross_50_200",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "sma50, sma200, close, open",
    "long": "sma50 > sma200 (golden cross), price pulls back near sma50, bullish candle",
    "short": "sma50 < sma200 (death cross), price rallies to sma50, bearish candle",
    "desc": "Golden/death cross SMA50/200 with pullback to SMA50 entry refinement",
    "source": "web:https://pippenguin.net/forex/learn-forex/golden-cross-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Pullback to SMA50 after golden/death cross regime established."""
    sma50 = ind["sma50"][pos]
    sma200 = ind["sma200"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    if nan(sma50, sma200, c, o):
        return None
    golden = sma50 > sma200
    death = sma50 < sma200
    near_sma50 = abs(c - sma50) / sma50 < 0.003
    bull_candle = c > o
    bear_candle = c < o
    if golden and near_sma50 and bull_candle:
        return "long"
    if death and near_sma50 and bear_candle:
        return "short"
    return None
