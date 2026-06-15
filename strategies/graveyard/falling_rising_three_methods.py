#!/usr/bin/env python3
"""falling_rising_three_methods -- Five-bar continuation: impulse bar (bar1), 3 small inside
bars (bars 2-4 contained within bar1 range), final bar closes beyond bar1 close.
J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.52."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "falling_rising_three_methods",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "continuation",
    "tf": "4h-1d",
    "indicators": "open,high,low,close",
    "long": "rising three: bar1 large up, 3 small bars inside bar1 range, bar5 close > bar1 close",
    "short": "falling three: bar1 large down, 3 small inside bars, bar5 close < bar1 close",
    "desc": "Rising/falling three methods: 5-bar flag continuation with final bar close breakout",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.52",
}

_SMALL_BODY_RATIO = 0.50   # inside bars body <= 50% of bar1 body


def signal(ind, pos, htf=None):
    """Rising/falling three methods continuation pattern."""
    if pos < 4:
        return None
    o1 = ind["open"][pos - 4]
    c1 = ind["close"][pos - 4]
    h1 = ind["high"][pos - 4]
    l1 = ind["low"][pos - 4]
    c5 = ind["close"][pos]
    o5 = ind["open"][pos]
    if nan(o1, c1, h1, l1, c5, o5):
        return None
    body1 = abs(c1 - o1)
    if body1 <= 0:
        return None

    # Check bars 2-4 are contained within bar1's range
    for k in range(1, 4):
        hk = ind["high"][pos - 4 + k]
        lk = ind["low"][pos - 4 + k]
        if nan(hk, lk):
            return None
        if hk > h1 or lk < l1:
            return None

    # Rising three: bar1 up, bar5 close > bar1 close
    if c1 > o1 and c5 > o5 and c5 > c1:
        return "long"
    # Falling three: bar1 down, bar5 close < bar1 close
    if c1 < o1 and c5 < o5 and c5 < c1:
        return "short"
    return None
