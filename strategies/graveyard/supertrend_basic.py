#!/usr/bin/env python3
"""supertrend_basic -- Supertrend direction flip entry. web:earnforex.com.

st_dir flips from -1 to +1 = long entry; from +1 to -1 = short entry.
Trail stop along st_line. Pure ATR-band trend-following flip.
No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_basic",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir",
    "long": "st_dir flips from -1 to +1",
    "short": "st_dir flips from +1 to -1",
    "desc": "Supertrend direction flip (basic)",
    "source": "web:https://www.earnforex.com/guides/free-forex-strategies-where-get-started/",
}


def signal(ind, pos, htf=None):
    """Supertrend direction flip."""
    sd = ind["st_dir"][pos]
    sdp = ind["st_dir"][pos - 1]
    if nan(sd, sdp):
        return None
    if sd == 1 and sdp == -1:
        return "long"
    if sd == -1 and sdp == 1:
        return "short"
    return None
