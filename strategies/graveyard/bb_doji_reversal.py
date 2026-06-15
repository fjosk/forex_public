#!/usr/bin/env python3
"""bb_doji_reversal -- BB extreme + prior doji + directional candle confirmation. zeta-zetra."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bb_doji_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_lo, bb_up, bb_mid, open, high, low, close",
    "long": "close < bb_lo AND close > open AND doji at pos-1 AND prior bearish at pos-2",
    "short": "close > bb_up AND close < open AND doji at pos-1 AND prior bullish at pos-2",
    "desc": "Bollinger Band extreme + doji reversal pattern: band touch, doji, then directional bar",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/youtube/bollinger_doji.html",
}


def signal(ind, pos, htf=None):
    """BB touch + doji + directional confirmation 3-bar pattern."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c2 = ind["close"][pos - 2]
    o2 = ind["open"][pos - 2]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    if nan(c, o, c1, o1, h1, l1, c2, o2, bb_lo, bb_up):
        return None
    bar_range1 = h1 - l1
    if bar_range1 <= 0:
        return None
    doji_thresh = 0.1 * bar_range1
    is_doji = abs(c1 - o1) < doji_thresh
    if not is_doji:
        return None
    if c < bb_lo and c > o and c2 < o2:
        return "long"
    if c > bb_up and c < o and c2 > o2:
        return "short"
    return None
