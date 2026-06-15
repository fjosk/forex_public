#!/usr/bin/env python3
"""donchian_morning_star_evening_star -- Morning/Evening Star reversal at Donchian channel boundary.

Pattern detection uses OHLC body comparisons inline. No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "donchian_morning_star_evening_star",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1d",
    "indicators": "dc_lo, dc_up, open, high, low, close",
    "long": "Morning Star 3-bar pattern near dc_lo AND close > high[-1]",
    "short": "Evening Star 3-bar pattern near dc_up AND close < low[-1]",
    "desc": "Donchian channel reversal: Morning/Evening Star pattern at the channel boundary",
    "source": "zeta-zetra.github.io/docs-forex-strategies-python/chatgpt/donchian_channel_candlestick.html",
}

# Buffer: allow price within 0.2% of channel boundary
_BUFFER = 0.002


def signal(ind, pos, htf=None):
    """Morning/Evening Star at Donchian channel boundary."""
    if pos < 2:
        return None
    o0 = ind["open"][pos]
    c0 = ind["close"][pos]
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    o2 = ind["open"][pos - 2]
    c2 = ind["close"][pos - 2]
    dc_lo = ind["dc_lo"][pos]
    dc_up = ind["dc_up"][pos]
    if nan(o0, c0, o1, c1, h1, l1, o2, c2, dc_lo, dc_up):
        return None

    # Body size for bar-1 indecision check
    body2 = abs(c2 - o2)
    body1 = abs(c1 - o1)
    # small body threshold: less than half of bar-2 body
    small_body_threshold = body2 * 0.5

    mid2 = (o2 + c2) / 2.0

    # Morning Star: bar-2 bearish large, bar-1 small body (indecision), bar-0 bullish above midpoint
    bar2_bear = c2 < o2
    bar1_small = body1 < small_body_threshold
    bar0_bull = c0 > o0 and c0 > mid2
    near_lower = c0 <= dc_lo * (1.0 + _BUFFER)
    if near_lower and bar2_bear and bar1_small and bar0_bull and c0 > h1:
        return "long"

    # Evening Star: bar-2 bullish large, bar-1 small body, bar-0 bearish below midpoint
    bar2_bull = c2 > o2
    bar0_bear = c0 < o0 and c0 < mid2
    near_upper = c0 >= dc_up * (1.0 - _BUFFER)
    if near_upper and bar2_bull and bar1_small and bar0_bear and c0 < l1:
        return "short"

    return None
