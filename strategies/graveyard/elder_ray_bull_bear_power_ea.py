#!/usr/bin/env python3
"""elder_ray_bull_bear_power_ea -- Elder Ray: bull/bear power dominance + EMA13 slope filter. MyCoder/Elder."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "elder_ray_bull_bear_power_ea",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "bull_power, bear_power, ema13",
    "long": "bull_power > abs(bear_power) AND EMA13 rising",
    "short": "abs(bear_power) > bull_power AND EMA13 falling",
    "desc": "Elder Ray Index: bull/bear power dominance with EMA13 direction filter",
    "source": "MyCoder Elder Ray MT4 strategy spec; Alexander Elder Elder Ray system",
}


def signal(ind, pos, htf=None):
    """Bull/bear power dominance gated by EMA13 slope direction."""
    bp = ind["bull_power"][pos]
    brp = ind["bear_power"][pos]
    e13 = ind["ema13"][pos]
    e13_1 = ind["ema13"][pos - 1]
    if nan(bp, brp, e13, e13_1):
        return None
    ema_rising = e13 > e13_1
    ema_falling = e13 < e13_1
    if bp > abs(brp) and ema_rising:
        return "long"
    if abs(brp) > bp and ema_falling:
        return "short"
    return None
