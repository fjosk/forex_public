#!/usr/bin/env python3
"""guppy_multiple_moving_average_gmma -- GMMA EA: short EMA group fully above/below long EMA group. theforexgeek."""
from strategies._common import nan, TREND, ALL_CLASSES

# Short group approximation: ema5, ema8, ema9, ema13 (for 3,5,8,10)
# Long group approximation: ema20, ema50, ema200 (for 30,45,60)

META = {
    "id": "guppy_multiple_moving_average_gmma",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema5, ema8, ema9, ema13, ema20, ema50, ema200",
    "long": "min(short group) > max(long group) with all short EMAs rising",
    "short": "max(short group) < min(long group) with all short EMAs falling",
    "desc": "Guppy GMMA EA: short ribbon fully separated above/below long ribbon",
    "source": "https://theforexgeek.com/gmma-indicator/",
}


def signal(ind, pos, htf=None):
    """GMMA short group vs long group full separation."""
    e5 = ind["ema5"][pos]
    e8 = ind["ema8"][pos]
    e9 = ind["ema9"][pos]
    e13 = ind["ema13"][pos]
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    e5_1 = ind["ema5"][pos - 1]
    e8_1 = ind["ema8"][pos - 1]
    e9_1 = ind["ema9"][pos - 1]
    e13_1 = ind["ema13"][pos - 1]
    if nan(e5, e8, e9, e13, e20, e50, e200, e5_1, e8_1, e9_1, e13_1):
        return None
    short_min = min(e5, e8, e9, e13)
    short_max = max(e5, e8, e9, e13)
    long_min = min(e20, e50, e200)
    long_max = max(e20, e50, e200)
    short_rising = e5 > e5_1 and e8 > e8_1 and e9 > e9_1 and e13 > e13_1
    short_falling = e5 < e5_1 and e8 < e8_1 and e9 < e9_1 and e13 < e13_1
    if short_min > long_max and short_rising:
        return "long"
    if short_max < long_min and short_falling:
        return "short"
    return None
