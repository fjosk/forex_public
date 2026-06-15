#!/usr/bin/env python3
"""dark_cloud_cover_bearish_two_candle_reversal -- Bearish dark cloud cover: after a long up
candle the next bar gaps above prior high then closes below the prior body midpoint.
J. Person, A Complete Guide to Technical Trading Tactics, p.49-50."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "dark_cloud_cover_bearish_two_candle_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close",
    "long": "none (short-only pattern)",
    "short": "bar1 long up body; bar2 opens above bar1 high and closes below bar1 body midpoint",
    "desc": "Dark cloud cover bearish reversal at top: gap up then close well into prior up body",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, p.49-50",
}


def signal(ind, pos, htf=None):
    """Dark cloud cover: short-only two-candle top reversal."""
    if pos < 1:
        return None
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    h1 = ind["high"][pos - 1]
    o2 = ind["open"][pos]
    c2 = ind["close"][pos]
    if nan(o1, c1, h1, o2, c2):
        return None
    # bar1: long up body
    if c1 <= o1:
        return None
    body1 = c1 - o1
    if body1 <= 0:
        return None
    midpoint = o1 + body1 / 2.0
    # bar2: opens above bar1 high, closes below midpoint (and above bar1 low side)
    if o2 > h1 and c2 < midpoint and c2 > o1:
        return "short"
    return None
