#!/usr/bin/env python3
"""previous_day_high_low_raid -- Previous Day High/Low Raid and Reverse. ICT / SMC community.

Price raids yesterday's high or low (sweeping stops), then closes back inside
the prior day's range. Entry in the reversal direction. Killzone filter applied.
Source: web:https://www.writofinance.com/previous-day-high-and-low-pdh-pdl/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "previous_day_high_low_raid",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "prev_dhh, prev_dll, close, high, low, atr, hour_utc",
    "long": "low spikes below prev_dll; close returns above it; London or NY AM killzone active",
    "short": "high spikes above prev_dhh; close returns below it; killzone active",
    "desc": "Previous Day High/Low raid and reversal with killzone filter",
    "source": "web:https://www.writofinance.com/previous-day-high-and-low-pdh-pdl/",
}


def signal(ind, pos, htf=None):
    """PDH/PDL raid: spike beyond prior day extreme then body return inside; killzone gated."""
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    pdh = ind["prev_dhh"][pos]
    pdl = ind["prev_dll"][pos]
    h = ind["hour_utc"][pos]
    if nan(c, lo, hi, pdh, pdl, h):
        return None

    # Killzone: London (07-10 UTC) or NY AM (12-15 UTC)
    in_kz = (7 <= h < 10) or (12 <= h < 15)
    if not in_kz:
        return None

    # Long: spike below PDL; body closes back above
    if lo < pdl and c > pdl:
        return "long"

    # Short: spike above PDH; body closes back below
    if hi > pdh and c < pdh:
        return "short"

    return None
