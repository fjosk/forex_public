#!/usr/bin/env python3
"""opening_range_breakout -- London open ORB: range first 15m (08:00-08:15 UTC), break after. web:howtotrade."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "opening_range_breakout",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "15m",
    "indicators": "hour_utc, high, low, close, open",
    "long": "full body close above London opening range high (08:00-08:15 UTC) during 08:15-12:00 UTC",
    "short": "full body close below opening range low during the entry window",
    "desc": "London ORB: define opening range first 15 min at 08:00 UTC, enter on full-body break",
    "source": "web:https://howtotrade.com/trading-strategies/opening-range-breakout-orb/",
}

# Opening range window: bars at hour_utc == 8, minute < 15 (on 15m bars: the 08:00 bar)
_OR_HOUR = 8
_OR_MINUTE_END = 15
_ENTRY_HOUR_END = 12
_LOOKBACK = 20  # bars to scan for the opening range definition


def signal(ind, pos, htf=None):
    """London ORB breakout."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    hu = ind["hour_utc"][pos]
    if nan(c, o, hu):
        return None
    hu_int = int(hu)
    # Entry window: 08:15 UTC to 12:00 UTC (after the range is defined)
    if not (_OR_HOUR <= hu_int <= _ENTRY_HOUR_END):
        return None
    # Build the opening range from the first bar(s) of this session at hour 8
    or_high = None
    or_low = None
    start = max(1, pos - _LOOKBACK)
    for i in range(start, pos):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            continue
        if int(h_i) == _OR_HOUR:
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
    # Full body above OR high (open and close both above)
    if c > or_high and o > or_high:
        return "long"
    # Full body below OR low
    if c < or_low and o < or_low:
        return "short"
    return None
