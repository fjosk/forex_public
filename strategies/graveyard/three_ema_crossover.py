#!/usr/bin/env python3
"""three_ema_crossover -- Triple EMA fan alignment (5/8/13): all three in order triggers entry. ForexFactory."""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "three_ema_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5, ema8, ema13",
    "long": "ema5 > ema8 > ema13 (bull fan) AND ema5 was not above ema8 prior bar (new alignment)",
    "short": "ema5 < ema8 < ema13 (bear fan) AND ema5 was not below ema8 prior bar",
    "desc": "Triple EMA fan (5/8/13): all three EMAs align in direction as entry trigger",
    "source": "web:https://www.forexfactory.com/thread/320335-yet-another-moving-average-crossover-system",
}


def signal(ind, pos, htf=None):
    """EMA5/8/13 fan alignment: entry on first bar where all three are ordered."""
    e5 = ind["ema5"][pos]
    e8 = ind["ema8"][pos]
    e13 = ind["ema13"][pos]
    e5p = ind["ema5"][pos - 1]
    e8p = ind["ema8"][pos - 1]
    e13p = ind["ema13"][pos - 1]
    if nan(e5, e8, e13, e5p, e8p, e13p):
        return None
    bull_fan = e5 > e8 > e13
    bear_fan = e5 < e8 < e13
    # New fan: was not fully aligned prior bar
    was_bull = e5p > e8p and e8p > e13p
    was_bear = e5p < e8p and e8p < e13p
    if bull_fan and not was_bull:
        return "long"
    if bear_fan and not was_bear:
        return "short"
    return None
