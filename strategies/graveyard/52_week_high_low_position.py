#!/usr/bin/env python3
"""52_week_high_low_position -- 52-week high/low breakout with MA alignment. web:asktraders.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "52_week_high_low_position",
    "cadences": ["swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "position",
    "tf": "1d",
    "indicators": "yr_high, yr_low, sma200, sma50, sma20, atr",
    "long": "weekly close exceeds 52-week high and SMA20 > SMA50 > SMA200",
    "short": "weekly close breaks below 52-week low and SMA20 < SMA50 < SMA200",
    "desc": "52-week high/low breakout with moving average stack confirmation",
    "source": "web:https://www.asktraders.com/learn-to-trade/trading-strategies/52-week-strategy/",
}


def signal(ind, pos, htf=None):
    """52-week high/low breakout with MA alignment."""
    c = ind["close"][pos]
    yh = ind["yr_high"][pos]
    yl = ind["yr_low"][pos]
    s20 = ind["sma20"][pos]
    s50 = ind["sma50"][pos]
    s200 = ind["sma200"][pos]
    if nan(c, yh, yl, s20, s50, s200):
        return None
    ma_bull = s20 > s50 and s50 > s200
    ma_bear = s20 < s50 and s50 < s200
    if c > yh and ma_bull:
        return "long"
    if c < yl and ma_bear:
        return "short"
    return None
