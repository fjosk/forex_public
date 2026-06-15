#!/usr/bin/env python3
"""atr_range_expansion_breakout -- ATR range expansion momentum entry. web:luxalgo.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "atr_range_expansion_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "atr, adx, body_mom, high, low, close, open",
    "long": "bullish expansion bar (range >= 1.5*ATR, close in upper half) and ADX >= 20",
    "short": "bearish expansion bar (range >= 1.5*ATR, close in lower half) and ADX >= 20",
    "desc": "ATR range expansion bar entry filtered by ADX",
    "source": "web:https://www.luxalgo.com/blog/rsi-indicator-trading-strategy-basics-and-rules/",
}


def signal(ind, pos, htf=None):
    """Range expansion: bar range >= 1.5 x ATR, close in upper/lower 40%, ADX >= 20."""
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    cl = ind["close"][pos]
    op = ind["open"][pos]
    atr = ind["atr"][pos]
    adx = ind["adx"][pos]
    if nan(hi, lo, cl, op, atr, adx):
        return None
    bar_range = hi - lo
    if bar_range <= 0 or atr <= 0:
        return None
    expansion = bar_range >= 1.5 * atr
    if not expansion or adx < 20:
        return None
    close_pct = (cl - lo) / bar_range
    bullish = cl > op
    bearish = cl < op
    if bullish and close_pct >= 0.6:
        return "long"
    if bearish and close_pct <= 0.4:
        return "short"
    return None
