#!/usr/bin/env python3
"""supertrend_atr_trend_following -- Supertrend direction flip entry. ForexTester/Netpicks.

st_dir flips from -1 to +1 = bullish (long entry); flips from +1 to -1 = bearish (short entry).
Uses the standard Supertrend (ATR 10 / multiplier 3.0 default in the engine).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_atr_trend_following",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir",
    "long": "st_dir flips from -1 to +1 (Supertrend turns bullish)",
    "short": "st_dir flips from +1 to -1 (Supertrend turns bearish)",
    "desc": "Supertrend ATR directional flip trend-following entry",
    "source": "web:https://forextester.com/blog/supertrend-indicator/; Olivier Seban",
}


def signal(ind, pos, htf=None):
    """Supertrend direction flip."""
    sd = ind["st_dir"][pos]
    sd1 = ind["st_dir"][pos - 1]
    if nan(sd, sd1):
        return None
    if sd == 1 and sd1 == -1:
        return "long"
    if sd == -1 and sd1 == 1:
        return "short"
    return None
