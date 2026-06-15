#!/usr/bin/env python3
"""asian_range_breakout -- Asian session range breakout at London open with H1 trend filter. web:forexfactory."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "asian_range_breakout",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close, sma20",
    "long": "H1 trend up (close > sma20), London open hour, price breaks above Asian session high",
    "short": "H1 trend down (close < sma20), price breaks below Asian session low",
    "desc": "Asian range breakout at London open filtered by H1 SMA20 trend direction",
    "source": "web:https://www.forexfactory.com/thread/457834-asian-breakout-with-trend",
}

_LOOKBACK = 60  # max bars to look back for Asian session bars (enough for ~1 day on 1h)


def signal(ind, pos, htf=None):
    """Asian range breakout filtered by H1 SMA20."""
    c = ind["close"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    hu = ind["hour_utc"][pos]
    s20 = ind["sma20"][pos]
    if nan(c, h, lo, hu, s20):
        return None
    # Only trigger during London open window: hours 7-13 UTC
    if not (7 <= int(hu) <= 13):
        return None
    # Build Asian session range from bars in current day where hour < 7
    asian_high = None
    asian_low = None
    start = max(1, pos - _LOOKBACK)
    for i in range(start, pos):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            continue
        if int(h_i) < 7:
            bar_h = ind["high"][i]
            bar_l = ind["low"][i]
            if nan(bar_h, bar_l):
                continue
            if asian_high is None or bar_h > asian_high:
                asian_high = bar_h
            if asian_low is None or bar_l < asian_low:
                asian_low = bar_l
    if asian_high is None or asian_low is None:
        return None
    # Trend filter + breakout
    if c > s20 and c > asian_high:
        return "long"
    if c < s20 and c < asian_low:
        return "short"
    return None
