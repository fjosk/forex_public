#!/usr/bin/env python3
"""london_open_killzone -- ICT London open killzone: Asian-range sweep then reversal. web:earnforex."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "london_open_killzone",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "15m",
    "indicators": "hour_utc, high, low, close",
    "long": "08-10 UTC window, bar wicked below Asian session low but closed above it (liquidity sweep + reversal)",
    "short": "bar wicked above Asian session high but closed below it during killzone",
    "desc": "ICT London killzone liquidity sweep: wick through Asian range extreme then close back inside",
    "source": "web:https://www.earnforex.com/forex-strategy/london-session-killzone-strategy/",
}

_LOOKBACK = 80  # bars to scan for Asian session range (00-08 UTC)
_KILLZONE_START = 8
_KILLZONE_END = 10


def signal(ind, pos, htf=None):
    """London killzone liquidity sweep and reversal."""
    c = ind["close"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    hu = ind["hour_utc"][pos]
    if nan(c, h, lo, hu):
        return None
    if not (_KILLZONE_START <= int(hu) <= _KILLZONE_END):
        return None
    # Asian session range: hours 0-7 UTC
    asian_high = None
    asian_low = None
    start = max(1, pos - _LOOKBACK)
    for i in range(start, pos):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            continue
        if int(h_i) < _KILLZONE_START:
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
    # Long: wick swept below Asian low but bar closed back above it (sweep + reversal)
    swept_low = lo < asian_low and c > asian_low
    # Short: wick swept above Asian high but bar closed back below it
    swept_high = h > asian_high and c < asian_high
    if swept_low:
        return "long"
    if swept_high:
        return "short"
    return None
