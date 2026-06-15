#!/usr/bin/env python3
"""asian_range_fade -- fade prior-range pierces during the quiet Asian session. Session class."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "asian_range_fade",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "session",
    "tf": "1h",
    "indicators": "hour_utc, prev_dhh, prev_dll, close",
    "long": "at 00:00-06:00 UTC close pierced below prior-day low (fade back up)",
    "short": "at 00:00-06:00 UTC close pierced above prior-day high (fade back down)",
    "desc": "Asian-session mean reversion: fade range pierces in thin liquidity",
    "source": "session-class:Asian-range fade",
}


def signal(ind, pos, htf=None):
    h = ind["hour_utc"][pos]
    if nan(h) or not (0 <= h <= 6):
        return None
    c, hh, ll = ind["close"][pos], ind["prev_dhh"][pos], ind["prev_dll"][pos]
    if nan(c, hh, ll):
        return None
    if c < ll:
        return "long"
    if c > hh:
        return "short"
    return None
