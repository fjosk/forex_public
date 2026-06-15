#!/usr/bin/env python3
"""bollinger_doji_reversal -- Bollinger Band + Doji Reversal Pattern. zeta-zetra."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bollinger_doji_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_lo, bb_up",
    "long": "close < bb_lo AND bullish candle AND prev doji AND bar[-2] bearish",
    "short": "close > bb_up AND bearish candle AND prev doji AND bar[-2] bullish",
    "desc": "Three-bar candlestick sequence at BB band: bearish -> doji -> directional reversal",
    "source": "github.com/zeta-zetra/code bollinger_doji.py",
}

_DOJI_THRESH = 0.1  # body < 10% of bar range counts as doji


def signal(ind, pos, htf=None):
    """Three-bar BB reversal: prior bar bearish/bullish, doji, then directional bar at band."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    c2 = ind["close"][pos - 2]
    o2 = ind["open"][pos - 2]
    h1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    bbl = ind["bb_lo"][pos]
    bbu = ind["bb_up"][pos]
    if nan(c, o, c1, o1, c2, o2, h1, lo1, bbl, bbu):
        return None
    bar_range1 = h1 - lo1
    body1 = abs(c1 - o1)
    doji = bar_range1 > 0 and body1 < bar_range1 * _DOJI_THRESH
    if c < bbl and c > o and doji and c2 < o2:
        return "long"
    if c > bbu and c < o and doji and c2 > o2:
        return "short"
    return None
