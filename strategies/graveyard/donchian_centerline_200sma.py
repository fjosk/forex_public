#!/usr/bin/env python3
"""donchian_centerline_200sma -- Donchian centerline cross filtered by SMA200. web:forextraininggroup."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "donchian_centerline_200sma",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, sma200, close",
    "long": "close above sma200 and close crosses above Donchian midline",
    "short": "close below sma200 and close crosses below Donchian midline",
    "desc": "Donchian centerline crossover with SMA200 trend filter",
    "source": "web:https://forextraininggroup.com/capturing-profits-using-donchian-channel-breakouts/",
}


def signal(ind, pos, htf=None):
    """Donchian centerline cross with SMA200 filter."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    dc_up = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    dc_up1 = ind["dc_up"][pos - 1]
    dc_lo1 = ind["dc_lo"][pos - 1]
    s200 = ind["sma200"][pos]
    if nan(c, c1, dc_up, dc_lo, dc_up1, dc_lo1, s200):
        return None
    dc_mid = (dc_up + dc_lo) / 2.0
    dc_mid1 = (dc_up1 + dc_lo1) / 2.0
    if c > s200 and _xup(c, c1, dc_mid, dc_mid1):
        return "long"
    if c < s200 and _xdn(c, c1, dc_mid, dc_mid1):
        return "short"
    return None
