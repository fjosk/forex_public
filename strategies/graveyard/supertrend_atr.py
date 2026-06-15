#!/usr/bin/env python3
"""supertrend_atr -- SuperTrend direction state entry (close vs bands). ntalegeofrey Python."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_atr",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir, st_line, close",
    "long": "st_dir == +1 (close above SuperTrend upper band, uptrend mode)",
    "short": "st_dir == -1 (close below SuperTrend lower band, downtrend mode)",
    "desc": "SuperTrend direction state: long while bullish, short while bearish",
    "source": "ntalegeofrey/Supertrend-Strategy-with-Python (Python, file: supertrend.py)",
}


def signal(ind, pos, htf=None):
    """Enter in the direction of the current SuperTrend state on a flip."""
    d = ind["st_dir"][pos]
    d1 = ind["st_dir"][pos - 1]
    if nan(d, d1):
        return None
    # Only fire on the flip bar (state change) to avoid re-entering on hold bars
    if d > 0 and d1 <= 0:
        return "long"
    if d < 0 and d1 >= 0:
        return "short"
    return None
