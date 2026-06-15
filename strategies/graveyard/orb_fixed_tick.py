#!/usr/bin/env python3
"""orb_fixed_tick -- Opening range breakout: price moves fixed ATR offset from day open.
trading_systems_and_methods_kaufman (Crabel).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "orb_fixed_tick",
    "cadences": ["day"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "day_open, atr, close",
    "long": "close > day_open + 0.25 * ATR (price has moved up from the open by a fixed offset)",
    "short": "close < day_open - 0.25 * ATR (price has moved down from the open by a fixed offset)",
    "desc": "Crabel fixed-tick opening range breakout: price advances from day open by ATR-scaled offset",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma",
}

_OFFSET_MULT = 0.25   # offset = 0.25 * ATR (proxy for a fixed tick offset)


def signal(ind, pos, htf=None):
    """Go long/short when close exceeds day_open +/- ATR-scaled offset."""
    c = ind["close"][pos]
    do = ind["day_open"][pos]
    atr = ind["atr"][pos]
    if nan(c, do, atr):
        return None
    offset = _OFFSET_MULT * atr
    if c > do + offset:
        return "long"
    if c < do - offset:
        return "short"
    return None
