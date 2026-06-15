#!/usr/bin/env python3
"""pivot_point_1m_bounce -- Daily pivot bounce: touch S1/PP/R1 with confirming candle. web:strategy-workspaceegiesresources.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_point_1m_bounce",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "5m",
    "indicators": "piv_p, piv_s1, piv_s2, piv_r1, piv_r2",
    "long": "close near piv_p/S1/S2 with bullish candle",
    "short": "close near piv_r1/R2 with bearish candle",
    "desc": "Daily pivot point bounce scalp at S1/PP/R1 levels",
    "source": "web:https://www.strategy-workspaceegiesresources.com/scalping-forex-strategies/136-1-min-scalping-with-pivot-points/",
}


def signal(ind, pos, htf=None):
    """Price touches a daily pivot level and closes with a confirming candle direction."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    pp = ind["piv_p"][pos]
    s1 = ind["piv_s1"][pos]
    s2 = ind["piv_s2"][pos]
    r1 = ind["piv_r1"][pos]
    r2 = ind["piv_r2"][pos]
    if nan(c, o, pp, s1, s2, r1, r2):
        return None
    pip2 = 0.0002
    near_support = abs(c - pp) < pip2 or abs(c - s1) < pip2 or abs(c - s2) < pip2
    near_resist = abs(c - r1) < pip2 or abs(c - r2) < pip2
    if near_support and c > o:
        return "long"
    if near_resist and c < o:
        return "short"
    return None
