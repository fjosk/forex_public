#!/usr/bin/env python3
"""evening_star_bearish_reversal -- Evening star three-candle top reversal: large up bar,
small star gapping above, large down bar closing below prior bar midpoint.
J. Person, A Complete Guide to Technical Trading Tactics, Index p.46-47."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "evening_star_bearish_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close",
    "long": "none (short-only pattern)",
    "short": "bar1 large up; bar2 small body gapping above bar1; bar3 large down closing below bar1 midpoint",
    "desc": "Evening star 3-candle bearish top reversal",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, p.46-47",
}

_STAR_BODY_RATIO = 0.30   # bar2 body <= 30% of bar1 body to qualify as star


def signal(ind, pos, htf=None):
    """Evening star: short on 3-bar top reversal pattern."""
    if pos < 2:
        return None
    o1 = ind["open"][pos - 2]
    c1 = ind["close"][pos - 2]
    o2 = ind["open"][pos - 1]
    c2 = ind["close"][pos - 1]
    o3 = ind["open"][pos]
    c3 = ind["close"][pos]
    if nan(o1, c1, o2, c2, o3, c3):
        return None
    # bar1: large up body
    body1 = c1 - o1
    if body1 <= 0:
        return None
    # bar2: small body above bar1 body (star)
    body2 = abs(c2 - o2)
    if body2 > _STAR_BODY_RATIO * body1:
        return None
    if min(o2, c2) <= max(o1, c1):
        return None   # star must gap above bar1 body
    # bar3: large down body closing below bar1 midpoint
    if c3 >= o3:
        return None
    midpoint1 = o1 + body1 / 2.0
    if c3 < midpoint1:
        return "short"
    return None
