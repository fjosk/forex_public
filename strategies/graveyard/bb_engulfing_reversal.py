#!/usr/bin/env python3
"""bb_engulfing_reversal -- BB band pierce + full engulfing candle reversal. zeta-zetra."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bb_engulfing_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_lo, bb_up, open, close",
    "long": "close < bb_lo AND bullish engulfing (current engulfs prior bearish bar)",
    "short": "close > bb_up AND bearish engulfing (current engulfs prior bullish bar)",
    "desc": "Bollinger Band pierce + engulfing reversal candle; zeta-zetra YouTube series",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/youtube/bollinger_engulfing.html",
}


def signal(ind, pos, htf=None):
    """BB extreme + full engulfing confirmation."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    if nan(c, o, c1, o1, bb_lo, bb_up):
        return None
    # Bullish engulfing: prior bearish, current bullish, fully engulfs
    bull_engulf = c1 < o1 and c > o and o < c1 and c > o1
    # Bearish engulfing: prior bullish, current bearish, fully engulfs
    bear_engulf = c1 > o1 and c < o and o > c1 and c < o1
    if c < bb_lo and bull_engulf:
        return "long"
    if c > bb_up and bear_engulf:
        return "short"
    return None
