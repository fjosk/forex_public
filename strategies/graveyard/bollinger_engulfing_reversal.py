#!/usr/bin/env python3
"""bollinger_engulfing_reversal -- Bollinger Band + Engulfing Candlestick Reversal. zeta-zetra."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bollinger_engulfing_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_lo, bb_up",
    "long": "close < bb_lo AND bullish engulfing pattern (body engulfs prior bearish body)",
    "short": "close > bb_up AND bearish engulfing pattern",
    "desc": "BB extreme + full engulfing candlestick confirmation for mean-reversion entry",
    "source": "github.com/zeta-zetra/code bollinger_engulfing.py",
}


def signal(ind, pos, htf=None):
    """BB band touch + full engulfing body for mean-reversion entry."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    bbl = ind["bb_lo"][pos]
    bbu = ind["bb_up"][pos]
    if nan(c, o, c1, o1, bbl, bbu):
        return None
    bull_engulf = (c > o and c1 < o1 and o < c1 and c > o1)
    bear_engulf = (c < o and c1 > o1 and o > c1 and c < o1)
    if c < bbl and bull_engulf:
        return "long"
    if c > bbu and bear_engulf:
        return "short"
    return None
