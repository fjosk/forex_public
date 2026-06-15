#!/usr/bin/env python3
"""break_of_structure_bos -- BOS continuation: close beyond prior fractal extreme.

Long BOS: close[pos] > frac_up_px[pos-1] (closes above the prior recorded swing high).
Short BOS: close[pos] < frac_dn_px[pos-1] (closes below the prior recorded swing low).
Entry is taken on the BOS bar itself (confirmation of trend continuation).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "break_of_structure_bos",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "15m, 1h, 4h",
    "indicators": "close, frac_up_px, frac_dn_px, hh_n, ll_n, atr",
    "long": "close breaks above prior fractal swing high (BOS up = trend continuation)",
    "short": "close breaks below prior fractal swing low (BOS down = trend continuation)",
    "desc": "Break of Structure (BOS) trend continuation: body close beyond prior swing extreme",
    "source": "web:https://innercircletrader.net/tutorials/break-of-structure-vs-change-of-character/",
}


def signal(ind, pos, htf=None):
    """BOS trend continuation signal."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    fup = ind["frac_up_px"][pos - 1]   # prior fractal swing high
    fdn = ind["frac_dn_px"][pos - 1]   # prior fractal swing low
    if nan(c, c1, fup, fdn):
        return None
    if c > fup and c1 <= fup:
        return "long"
    if c < fdn and c1 >= fdn:
        return "short"
    return None
