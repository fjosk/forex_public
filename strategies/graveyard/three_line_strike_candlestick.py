#!/usr/bin/env python3
"""three_line_strike_candlestick -- Three consecutive directional bars followed by engulfing reversal candle.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "three_line_strike_candlestick",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "open, high, low, close",
    "long": "3 prior bars bearish+lower highs+lower lows, current bull engulfing closing above bar[-3].open",
    "short": "3 prior bars bullish+higher highs+higher lows, current bear engulfing closing below bar[-3].open",
    "desc": "Three line strike reversal: three-bar sequence exhaustion followed by engulfing reversal candle",
    "source": "zeta-zetra.github.io/docs-forex-strategies-python/youtube/three_line_strike.html",
}


def signal(ind, pos, htf=None):
    """Three line strike reversal pattern."""
    if pos < 3:
        return None
    o0 = ind["open"][pos]
    c0 = ind["close"][pos]
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    o2 = ind["open"][pos - 2]
    c2 = ind["close"][pos - 2]
    h2 = ind["high"][pos - 2]
    l2 = ind["low"][pos - 2]
    o3 = ind["open"][pos - 3]
    c3 = ind["close"][pos - 3]
    h3 = ind["high"][pos - 3]
    l3 = ind["low"][pos - 3]
    if nan(o0, c0, o1, c1, h1, l1, o2, c2, h2, l2, o3, c3, h3, l3):
        return None

    # Long: 3 prior bearish bars, progressively lower highs and lows, then bull engulfing
    prior_bearish_l = c3 < o3 and c2 < o2 and c1 < o1
    lower_highs = h3 > h2 > h1
    lower_lows = l3 > l2 > l1
    bull_engulf = c0 > o0 and o0 < c1 and c0 > o3
    if prior_bearish_l and lower_highs and lower_lows and bull_engulf:
        return "long"

    # Short: 3 prior bullish bars, progressively higher highs and lows, then bear engulfing
    prior_bullish_s = c3 > o3 and c2 > o2 and c1 > o1
    higher_highs = h3 < h2 < h1
    higher_lows = l3 < l2 < l1
    bear_engulf = c0 < o0 and o0 > c1 and c0 < o3
    if prior_bullish_s and higher_highs and higher_lows and bear_engulf:
        return "short"

    return None
