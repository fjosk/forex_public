#!/usr/bin/env python3
"""year_high_proximity_momentum -- 52-week high proximity momentum (George & Hwang 2004).

Long when price is within 5% of its 52-week high (anchoring momentum signal).
Short when price is below 75% of its 52-week high (far from recent peak = negative momentum).
SMA200 confirmation filter.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "year_high_proximity_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "yr_high, close, sma200",
    "long": "close / yr_high > 0.95 and close > SMA200 (near 52-week high)",
    "short": "close / yr_high < 0.75 and close < SMA200 (far below 52-week high)",
    "desc": "52-week high proximity anchoring momentum (George & Hwang 2004)",
    "source": "web:https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf; Journal of Finance (2004)",
}


def signal(ind, pos, htf=None):
    """52-week high proximity signal."""
    c = ind["close"][pos]
    yh = ind["yr_high"][pos]
    s200 = ind["sma200"][pos]
    if nan(c, yh, s200) or yh == 0:
        return None
    ratio = c / yh
    if ratio > 0.95 and c > s200:
        return "long"
    if ratio < 0.75 and c < s200:
        return "short"
    return None
