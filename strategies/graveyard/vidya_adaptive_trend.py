#!/usr/bin/env python3
"""vidya_adaptive_trend -- VIDYA adaptive MA trend: slope + CMO momentum filter. web:trendfollowingsystem.com.

VIDYA adapts its smoothing to CMO (momentum). Price above VIDYA + positive VIDYA slope +
positive CMO = long. Reverse for short. No volume dependency.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "vidya_adaptive_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "vidya, cmo",
    "long": "close > vidya AND vidya rising AND cmo > 0 (fresh cross above from below)",
    "short": "close < vidya AND vidya falling AND cmo < 0",
    "desc": "VIDYA Variable Index Dynamic Average trend with CMO momentum filter",
    "source": "web:https://www.trendfollowingsystem.com/variable-index-dynamic-average-vidya/",
}


def signal(ind, pos, htf=None):
    """VIDYA slope + CMO confirmation trend entry."""
    c = ind["close"][pos]
    cp = ind["close"][pos - 1]
    v = ind["vidya"][pos]
    vp = ind["vidya"][pos - 1]
    cmo = ind["cmo"][pos]
    if nan(c, cp, v, vp, cmo):
        return None
    vidya_up = v > vp
    vidya_dn = v < vp
    # require fresh cross (was below, now above) to avoid holding entire trend
    just_crossed_up = c > v and cp <= vp
    just_crossed_dn = c < v and cp >= vp
    if just_crossed_up and vidya_up and cmo > 0:
        return "long"
    if just_crossed_dn and vidya_dn and cmo < 0:
        return "short"
    return None
