#!/usr/bin/env python3
"""pinbar_reversal -- Three-bar pin bar reversal pattern (left eye / nose / right eye). web:earnforex.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pinbar_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "open, high, low, close",
    "long": "bullish 3-bar pin: nose protrudes below left eye, body in top 1/4 of nose bar",
    "short": "bearish 3-bar pin: nose protrudes above left eye, body in bottom 1/4 of nose bar",
    "desc": "Three-bar pin bar (left eye / nose / right eye) reversal pattern",
    "source": "web:https://www.earnforex.com/forex-strategy/pinbar-trading-system/",
}


def signal(ind, pos, htf=None):
    """Three-bar pinbar reversal: pos-2=left eye, pos-1=nose, pos=right eye confirmation."""
    o2, h2, lo2, c2 = ind["open"][pos - 2], ind["high"][pos - 2], ind["low"][pos - 2], ind["close"][pos - 2]
    o1, h1, lo1, c1 = ind["open"][pos - 1], ind["high"][pos - 1], ind["low"][pos - 1], ind["close"][pos - 1]
    c0 = ind["close"][pos]
    if nan(o2, h2, lo2, c2, o1, h1, lo1, c1, c0):
        return None
    nose_rng1 = h1 - lo1
    if nose_rng1 <= 0:
        return None
    # Bullish pin: left eye is down bar, nose protrudes below, body in top 1/4 of nose
    le_bearish = c2 < o2
    nose_lo_prot = lo1 < lo2
    nose_body_top = min(o1, c1) > lo1 + 0.75 * nose_rng1
    nose_inside_le = o1 < h2 and o1 > lo2 and c1 < h2 and c1 > lo2
    if le_bearish and nose_lo_prot and nose_body_top and nose_inside_le and c0 > c2:
        return "long"
    # Bearish pin: left eye is up bar, nose protrudes above, body in bottom 1/4 of nose
    le_bullish = c2 > o2
    nose_hi_prot = h1 > h2
    nose_body_bot = max(o1, c1) < lo1 + 0.25 * nose_rng1
    nose_inside_le2 = o1 < h2 and o1 > lo2 and c1 < h2 and c1 > lo2
    if le_bullish and nose_hi_prot and nose_body_bot and nose_inside_le2 and c0 < c2:
        return "short"
    return None
