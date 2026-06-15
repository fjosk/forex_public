#!/usr/bin/env python3
"""round_number_par_breakout -- Round-number par breakout (cross of 100/200/300 level).
reminiscences_of_a_stock_operator.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "round_number_par_breakout",
    "cadences": ["swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "round_step, close",
    "long": "close crosses above the nearest major round-step grid level for the first time (new par level crossed)",
    "short": "close crosses below the nearest major round-step grid level",
    "desc": "Reminiscences par breakout: first cross of a major round-number level with follow-through",
    "source": "book: reminiscences_of_a_stock_operator_edwin_lefevre",
}


def signal(ind, pos, htf=None):
    """Close crosses a round_step grid boundary."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    rs = ind["round_step"][pos]
    if nan(c, c1, rs) or rs <= 0:
        return None
    import math
    lev_c = math.floor(c / rs) * rs
    lev_c1 = math.floor(c1 / rs) * rs
    if lev_c > lev_c1:
        return "long"
    if lev_c < lev_c1:
        return "short"
    return None
