#!/usr/bin/env python3
"""donchian_20_sma_filter -- Donchian 20 breakout + SMA10/SMA20 trend alignment. web:github/hasnocool."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "donchian_20_sma_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "dc_up, dc_lo, sma10, sma20",
    "long": "close > dc_up and sma10 > sma20 (trend aligned up)",
    "short": "close < dc_lo and sma20 > sma10 (trend aligned down)",
    "desc": "Donchian 20 breakout with SMA10/SMA20 trend alignment filter (proxy for SMA8/SMA32)",
    "source": "web:https://github.com/hasnocool/tradingview-pine-scripts",
}


def signal(ind, pos, htf=None):
    """DC breakout + SMA fast/slow trend alignment."""
    cl = ind["close"][pos]
    dcu = ind["dc_up"][pos]
    dcl = ind["dc_lo"][pos]
    sf = ind["sma10"][pos]
    ss = ind["sma20"][pos]
    if nan(cl, dcu, dcl, sf, ss):
        return None
    if cl > dcu and sf > ss:
        return "long"
    if cl < dcl and ss > sf:
        return "short"
    return None
