#!/usr/bin/env python3
"""chandelier_exit_entry_signal -- Chandelier Exit repurposed as entry signal on direction flip. yuj123 / NJiHin.

chand_dir flip (+1 to -1 or vice versa) signals the entry. The chandelier direction itself is the
trailing stop proxy (engine ATR exit takes over once entered).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "chandelier_exit_entry_signal",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "chand_dir, atr",
    "long": "chand_dir flips to +1 from -1 (CE turned bullish: price crossed above chandelier long-stop)",
    "short": "chand_dir flips to -1 from +1 (CE turned bearish: price crossed below chandelier short-stop)",
    "desc": "Chandelier Exit as entry signal: direction flip entry with opposite-signal exit",
    "source": "https://github.com/yuj123/buy_cross_chandelier_exit; https://github.com/NJiHin/TA_Chandelier",
}


def signal(ind, pos, htf=None):
    """Chandelier direction flip entry signal."""
    d = ind["chand_dir"][pos]
    d1 = ind["chand_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d == 1 and d1 == -1:
        return "long"
    if d == -1 and d1 == 1:
        return "short"
    return None
