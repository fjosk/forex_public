#!/usr/bin/env python3
"""ssl_hybrid_trend -- SSL Hybrid direction flip as entry signal. web:earnforex.com.

Clean flip-based system: ssl_hlv flips from -1 to +1 = long, from +1 to -1 = short.
Exit on opposite flip. No additional filters; pure SSL channel signal.
No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ssl_hybrid_trend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ssl_hlv",
    "long": "ssl_hlv flips from -1 to +1",
    "short": "ssl_hlv flips from +1 to -1",
    "desc": "SSL Hybrid trend channel direction flip",
    "source": "web:https://www.earnforex.com/guides/free-forex-strategies-where-get-started/",
}


def signal(ind, pos, htf=None):
    """SSL channel direction flip entry."""
    hlv = ind["ssl_hlv"][pos]
    hlvp = ind["ssl_hlv"][pos - 1]
    if nan(hlv, hlvp):
        return None
    if hlv == 1 and hlvp == -1:
        return "long"
    if hlv == -1 and hlvp == 1:
        return "short"
    return None
