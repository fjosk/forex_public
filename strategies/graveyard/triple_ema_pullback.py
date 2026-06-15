#!/usr/bin/env python3
"""triple_ema_pullback -- Triple EMA 8/21/50 fan-out pullback with rejection. web:mirapip.com.

Three EMAs in fan-out alignment. Wait for price to pull back to touch ema8 or ema21;
enter on rejection (candle wicked through EMA but closed above/below it).
No volume dependency.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "triple_ema_pullback",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema8, ema21, ema50, low, high, close",
    "long": "ema8 > ema21 > ema50 AND low <= ema21 AND close > ema8 (pullback + rejection)",
    "short": "ema8 < ema21 < ema50 AND high >= ema21 AND close < ema8 (pullback + rejection)",
    "desc": "Triple EMA 8/21/50 fan-out with pullback-rejection entry",
    "source": "web:https://mirapip.com/three-ema-strategy-in-forex/",
}


def signal(ind, pos, htf=None):
    """EMA fan-out pullback and rejection entry."""
    e8 = ind["ema8"][pos]
    e21 = ind["ema21"][pos]
    e50 = ind["ema50"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    c = ind["close"][pos]
    if nan(e8, e21, e50, lo, hi, c):
        return None
    bull_fan = e8 > e21 > e50
    bear_fan = e8 < e21 < e50
    # long: pullback to ema8 or ema21, rejection close above ema8
    if bull_fan and lo <= e21 and c > e8:
        return "long"
    # short: pullback to ema8 or ema21, rejection close below ema8
    if bear_fan and hi >= e21 and c < e8:
        return "short"
    return None
