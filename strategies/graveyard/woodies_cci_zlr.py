#!/usr/bin/env python3
"""woodies_cci_zlr -- Woodies CCI Zero-Line Reject: CCI approaches zero then bounces. web:forexfactory.com."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "woodies_cci_zlr",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "15m",
    "indicators": "cci",
    "long": "CCI below zero, approached zero (was between -100 and 0), now turns up still below zero",
    "short": "CCI above zero, approached zero (was between 0 and 100), now turns down still above zero",
    "desc": "Woodies CCI Zero-Line Reject -- bounce off zero line without crossing",
    "source": "web:https://www.forexfactory.com/thread/683595-woodies-cci-system",
}


def signal(ind, pos, htf=None):
    """CCI zero-line reject: approached zero then bounced without crossing."""
    c2 = ind["cci"][pos - 2]
    c1 = ind["cci"][pos - 1]
    c0 = ind["cci"][pos]
    if nan(c2, c1, c0):
        return None
    # ZLR long: was between -100 and 0, approached zero (c1 > -100 and c1 < 10), now turning up, still below 0
    if c2 > -100 and c1 < 10 and c0 > c1 and c0 < 0:
        return "long"
    # ZLR short: was between 0 and 100, approached zero (c1 < 100 and c1 > -10), now turning down, still above 0
    if c2 < 100 and c1 > -10 and c0 < c1 and c0 > 0:
        return "short"
    return None
