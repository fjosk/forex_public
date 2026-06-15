#!/usr/bin/env python3
"""donchian_20_channel_reversal -- Donchian 20 confirmed breakout (2-bar rising/falling). web:github/hasnocool."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "donchian_20_channel_reversal",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "dc_up, dc_lo",
    "long": "dc_up rising for 2 consecutive bars (dc_up > dc_up[1] > dc_up[2])",
    "short": "dc_lo falling for 2 consecutive bars (dc_lo < dc_lo[1] < dc_lo[2])",
    "desc": "Donchian 20-period confirmed breakout: 2-bar rising upper or falling lower band",
    "source": "web:https://github.com/hasnocool/tradingview-pine-scripts",
}


def signal(ind, pos, htf=None):
    """DC confirmed: upper band rising 2 bars = long; lower band falling 2 bars = short."""
    if pos < 2:
        return None
    dcu = ind["dc_up"][pos]
    dcu1 = ind["dc_up"][pos - 1]
    dcu2 = ind["dc_up"][pos - 2]
    dcl = ind["dc_lo"][pos]
    dcl1 = ind["dc_lo"][pos - 1]
    dcl2 = ind["dc_lo"][pos - 2]
    if nan(dcu, dcu1, dcu2, dcl, dcl1, dcl2):
        return None
    if dcu > dcu1 and dcu1 > dcu2:
        return "long"
    if dcl < dcl1 and dcl1 < dcl2:
        return "short"
    return None
