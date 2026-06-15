#!/usr/bin/env python3
"""donchian_n_bar_breakout -- Donchian N-bar breakout (QuanDuong / Tom Basso). web:mql5.com/49272."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "donchian_n_bar_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "dc_up, dc_lo, close",
    "long": "close > dc_up[pos-1] (N-bar high break)",
    "short": "close < dc_lo[pos-1] (N-bar low break)",
    "desc": "Donchian N-bar breakout: buy above prior N-bar high, sell below N-bar low (QuanDuong/Tom Basso)",
    "source": "web:https://www.mql5.com/en/code/49272",
}


def signal(ind, pos, htf=None):
    """N-bar Donchian breakout: close vs prior-bar dc_up/dc_lo."""
    cl = ind["close"][pos]
    dcu1 = ind["dc_up"][pos - 1]
    dcl1 = ind["dc_lo"][pos - 1]
    if nan(cl, dcu1, dcl1):
        return None
    if cl > dcu1:
        return "long"
    if cl < dcl1:
        return "short"
    return None
