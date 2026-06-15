#!/usr/bin/env python3
"""supertrend_atr_trailing_signal -- SuperTrend direction flip entry signal. ntalegeofrey Python."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_atr_trailing_signal",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir, st_line",
    "long": "st_dir flips from -1 to +1 (SuperTrend turns bullish)",
    "short": "st_dir flips from +1 to -1 (SuperTrend turns bearish)",
    "desc": "SuperTrend ATR trailing stop signal: enter on direction flip; st_line is the trailing stop",
    "source": "ntalegeofrey/Supertrend-Strategy-with-Python (Python); luxalgo.com formula reference",
}


def signal(ind, pos, htf=None):
    """Enter on SuperTrend direction flip."""
    d = ind["st_dir"][pos]
    d1 = ind["st_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d > 0 and d1 <= 0:
        return "long"
    if d < 0 and d1 >= 0:
        return "short"
    return None
