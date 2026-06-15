#!/usr/bin/env python3
"""london_breakout_asian_range -- London open breakout of Asian session range. web:market-bulls."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "london_breakout_asian_range",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close",
    "long": "London open window (07-09 UTC), close breaks above Asian session high (00-07 UTC)",
    "short": "London open window, close breaks below Asian session low",
    "desc": "London open breakout of the Asian session high/low range",
    "source": "web:https://market-bulls.com/london-breakout-strategy/",
}

_LOOKBACK = 60  # bars to scan for Asian session range


def signal(ind, pos, htf=None):
    """London open breakout of Asian session range."""
    c = ind["close"][pos]
    hu = ind["hour_utc"][pos]
    if nan(c, hu):
        return None
    if not (7 <= int(hu) <= 9):
        return None
    # Scan recent bars for Asian session (hour_utc 0-6)
    asian_high = None
    asian_low = None
    start = max(1, pos - _LOOKBACK)
    for i in range(start, pos):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            continue
        if int(h_i) < 7:
            bh = ind["high"][i]
            bl = ind["low"][i]
            if nan(bh, bl):
                continue
            if asian_high is None or bh > asian_high:
                asian_high = bh
            if asian_low is None or bl < asian_low:
                asian_low = bl
    if asian_high is None or asian_low is None:
        return None
    if c > asian_high:
        return "long"
    if c < asian_low:
        return "short"
    return None
