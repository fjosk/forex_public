#!/usr/bin/env python3
"""donchian_scalping_h1_ea -- Donchian channel scalping EA on H1 (afabiani). web:mql5.com/46774."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "donchian_scalping_h1_ea",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "dc_up, dc_lo, close",
    "long": "close > dc_up[pos] and close[pos-1] <= dc_up[pos-1] (new break above DC upper)",
    "short": "close < dc_lo[pos] and close[pos-1] >= dc_lo[pos-1] (new break below DC lower)",
    "desc": "Donchian Channel scalping EA (afabiani H1): fresh cross of current-bar channel boundary",
    "source": "web:https://www.mql5.com/en/code/46774",
}


def signal(ind, pos, htf=None):
    """Fresh DC cross on current bar: close vs current and prior dc_up/dc_lo."""
    cl = ind["close"][pos]
    cl1 = ind["close"][pos - 1]
    dcu = ind["dc_up"][pos]
    dcl = ind["dc_lo"][pos]
    dcu1 = ind["dc_up"][pos - 1]
    dcl1 = ind["dc_lo"][pos - 1]
    if nan(cl, cl1, dcu, dcl, dcu1, dcl1):
        return None
    if cl > dcu and cl1 <= dcu1:
        return "long"
    if cl < dcl and cl1 >= dcl1:
        return "short"
    return None
