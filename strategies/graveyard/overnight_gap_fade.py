#!/usr/bin/env python3
"""overnight_gap_fade -- fade the UTC-day open gap back toward the prior close. Session class."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "overnight_gap_fade",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "hour_utc, day_open, prev_dhc, prev_dlc, close",
    "long": "early session, day opened below the prior-day close range (gap down) -> fade up",
    "short": "early session, day opened above the prior-day close range (gap up) -> fade down",
    "desc": "Overnight gap fade at the UTC day open",
    "source": "session-class:gap fade",
}


def signal(ind, pos, htf=None):
    h = ind["hour_utc"][pos]
    if nan(h) or not (0 <= h <= 3):
        return None
    do, c = ind["day_open"][pos], ind["close"][pos]
    phc, plc = ind["prev_dhc"][pos], ind["prev_dlc"][pos]
    if nan(do, c, phc, plc):
        return None
    # gap down (opened below prior close range) and still below -> expect mean reversion up
    if do < plc and c < plc:
        return "long"
    if do > phc and c > phc:
        return "short"
    return None
