#!/usr/bin/env python3
"""inside_day_narrowest_range_breakout -- Inside-day narrowest-range (NR) breakout: when today is an inside day AND has the narrowest range of the last 5 bars, a close outside the inside-day range signals a breakout. Tharp/Van Tharp Ch.7.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_day_narrowest_range_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "high, low, close, rng5",
    "long": "Inside day with narrowest range (range <= rng5 low) and close breaks above inside-day high",
    "short": "Inside day with narrowest range and close breaks below inside-day low",
    "desc": "Inside-day narrowest-range (NR) breakout: inside day with compressed range predicts explosive move in breakout direction",
    "source": "trade_your_way_to_financial_freedom -- Ch.7 Volatility narrow-range setup",
}


def signal(ind, pos, htf=None):
    """Inside day with narrow range: close breaks out of the inside bar."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c = ind["close"][pos]
    # rng5 = 5-bar high-low range; use as the reference narrow-range threshold
    r5 = ind["rng5"][pos]
    if nan(h, l, h1, l1, c, r5):
        return None
    # inside day condition
    is_inside = h < h1 and l > l1
    if not is_inside:
        return None
    # narrowest range: today's range must be <= rng5 (i.e. at or near the 5-bar minimum)
    today_range = h - l
    # rng5 is the range of the last 5 bars (max-high minus min-low); today being narrower
    # than half of rng5 is a reasonable proxy for narrowest-of-5
    if today_range >= 0.5 * r5:
        return None
    # breakout: close outside the inside bar's range
    if c > h1:
        return "long"
    if c < l1:
        return "short"
    return None
