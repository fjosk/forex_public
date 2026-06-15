#!/usr/bin/env python3
"""the_impulse_system -- Elder Impulse System: both EMA13 rising AND MACD-Histogram rising = long (green bar); both falling = short (red bar). Elder.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "the_impulse_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "ema13, macd_hist",
    "long": "EMA13 rising AND MACD-Histogram rising (both in-gear up = green impulse bar)",
    "short": "EMA13 falling AND MACD-Histogram falling (both in-gear down = red impulse bar)",
    "desc": "Elder Impulse System: simultaneous EMA13 and MACD-H agreement required for entry",
    "source": "Elder, Come Into My Trading Room, Ch.6 The Impulse System Entries/Exits, pp.157-161",
}


def signal(ind, pos, htf=None):
    """Both EMA13 and MACD-Histogram must agree for entry."""
    if pos < 1:
        return None
    e = ind["ema13"][pos]
    e1 = ind["ema13"][pos - 1]
    h = ind["macd_hist"][pos]
    h1 = ind["macd_hist"][pos - 1]
    if nan(e, e1, h, h1):
        return None
    if e > e1 and h > h1:
        return "long"
    if e < e1 and h < h1:
        return "short"
    return None
