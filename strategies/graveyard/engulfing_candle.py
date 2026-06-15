#!/usr/bin/env python3
"""engulfing_candle -- Bullish/bearish engulfing candle reversal pattern. web:admiralmarkets."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "engulfing_candle",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "open, close",
    "long": "prior candle bearish, current candle bullish body fully engulfs prior body",
    "short": "prior candle bullish, current candle bearish body fully engulfs prior body",
    "desc": "Two-candle engulfing reversal: current body engulfs prior body in the opposite direction",
    "source": "web:https://admiralmarkets.com/education/articles/forex-strategy/best-forex-trading-strategies-that-work",
}


def signal(ind, pos, htf=None):
    """Bullish/bearish engulfing candlestick pattern."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    if nan(c, o, c1, o1):
        return None
    prior_bearish = c1 < o1
    curr_bullish = c > o
    body_engulfs_bull = o <= c1 and c >= o1
    if prior_bearish and curr_bullish and body_engulfs_bull:
        return "long"
    prior_bullish = c1 > o1
    curr_bearish = c < o
    body_engulfs_bear = o >= c1 and c <= o1
    if prior_bullish and curr_bearish and body_engulfs_bear:
        return "short"
    return None
