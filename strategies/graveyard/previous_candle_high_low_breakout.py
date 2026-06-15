#!/usr/bin/env python3
"""previous_candle_high_low_breakout -- Close breaks above prior bar high or below prior bar low. Forex Factory EA."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "previous_candle_high_low_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "high, low, close",
    "long": "close > high[pos-1] (breaks above prior bar high)",
    "short": "close < low[pos-1] (breaks below prior bar low)",
    "desc": "Previous candle high/low breakout: close clears prior bar extreme",
    "source": "web:https://www.forexfactory.com/thread/546575-previous-candle-high-low-ea",
}


def signal(ind, pos, htf=None):
    """Break above prior bar high (long) or below prior bar low (short)."""
    c = ind["close"][pos]
    prev_hi = ind["high"][pos - 1]
    prev_lo = ind["low"][pos - 1]
    if nan(c, prev_hi, prev_lo):
        return None
    if c > prev_hi:
        return "long"
    if c < prev_lo:
        return "short"
    return None
