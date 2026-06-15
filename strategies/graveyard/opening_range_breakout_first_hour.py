#!/usr/bin/env python3
"""opening_range_breakout_first_hour -- London ORB first hour (07-08 UTC range). web:fbs."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "opening_range_breakout_first_hour",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "hour_utc, high, low, close",
    "long": "close above London first-hour range high (07:00-08:00 UTC) during 08:00-10:00 UTC",
    "short": "close below London first-hour range low during entry window",
    "desc": "Opening range breakout using the first London hour (07:00-08:00 UTC) as the range",
    "source": "web:https://fbs.com/fbs-academy/traders-blog/opening-range-breakout-trading-strategy",
}

_RANGE_HOUR = 7
_ENTRY_START = 8
_ENTRY_END = 10
_LOOKBACK = 30


def signal(ind, pos, htf=None):
    """London first-hour ORB breakout."""
    c = ind["close"][pos]
    hu = ind["hour_utc"][pos]
    if nan(c, hu):
        return None
    hu_int = int(hu)
    if not (_ENTRY_START <= hu_int <= _ENTRY_END):
        return None
    or_high = None
    or_low = None
    start = max(1, pos - _LOOKBACK)
    for i in range(start, pos):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            continue
        if int(h_i) == _RANGE_HOUR:
            bh = ind["high"][i]
            bl = ind["low"][i]
            if nan(bh, bl):
                continue
            if or_high is None or bh > or_high:
                or_high = bh
            if or_low is None or bl < or_low:
                or_low = bl
    if or_high is None or or_low is None:
        return None
    rng = or_high - or_low
    if rng <= 0:
        return None
    # Minimum range filter: at least 0.2% of price
    if rng / (or_low + 1e-10) < 0.002:
        return None
    if c > or_high:
        return "long"
    if c < or_low:
        return "short"
    return None
