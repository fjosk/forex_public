#!/usr/bin/env python3
"""pivot_point_breakout -- Pivot R1/S1 confirmed close breakout. web:babypips.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "pivot_point_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "piv_r1, piv_s1, close",
    "long": "close breaks above piv_r1 (prior close was at or below R1)",
    "short": "close breaks below piv_s1 (prior close was at or above S1)",
    "desc": "Daily pivot R1/S1 confirmed close breakout",
    "source": "web:https://www.babypips.com/learn/forex/playing-the-breaks-with-pivot-points",
}


def signal(ind, pos, htf=None):
    """Pivot R1/S1 breakout on confirmed close."""
    c, c1 = ind["close"][pos], ind["close"][pos - 1]
    r1, r1_1 = ind["piv_r1"][pos], ind["piv_r1"][pos - 1]
    s1, s1_1 = ind["piv_s1"][pos], ind["piv_s1"][pos - 1]
    if nan(c, c1, r1, r1_1, s1, s1_1):
        return None
    if c > r1 and c1 <= r1_1:
        return "long"
    if c < s1 and c1 >= s1_1:
        return "short"
    return None
