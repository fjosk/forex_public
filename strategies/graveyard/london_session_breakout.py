#!/usr/bin/env python3
"""london_session_breakout -- London session breakout of Asian box (00-07 GMT). web:forexfactory."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "london_session_breakout",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close",
    "long": "price breaks above Asian session high (00-07 GMT) during London hours (07-14 UTC)",
    "short": "price breaks below Asian session low during London hours",
    "desc": "Simple London session breakout of the Asian box (00:00-07:00 GMT high/low)",
    "source": "web:https://www.forexfactory.com/thread/230640-a-simple-london-breakout",
}

_LOOKBACK = 60


def signal(ind, pos, htf=None):
    """London session breakout of Asian box."""
    c = ind["close"][pos]
    hu = ind["hour_utc"][pos]
    if nan(c, hu):
        return None
    # London window: 07:00-14:00 UTC
    if not (7 <= int(hu) <= 14):
        return None
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
