#!/usr/bin/env python3
"""evening_star_morning_star_3_candle_reversal -- Three-candle star reversal pair: morning star
(bullish bottom) and evening star (bearish top); candle2 gaps from candle1 body.
J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.46-48."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "evening_star_morning_star_3_candle_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,close",
    "long": "morning star: bar1 large down, bar2 small body below bar1, bar3 large up closes above bar1 midpoint",
    "short": "evening star: bar1 large up, bar2 small body above bar1, bar3 large down closes below bar1 midpoint",
    "desc": "Evening/morning star 3-candle reversal with gap-away star",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.46-48",
}

_STAR_BODY_RATIO = 0.30   # star bar body <= 30% of bar1 body


def signal(ind, pos, htf=None):
    """Morning star (long) or evening star (short) 3-candle reversal."""
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

    body1 = abs(c1 - o1)
    if body1 <= 0:
        return None
    body2 = abs(c2 - o2)
    midpoint1 = min(o1, c1) + body1 / 2.0

    # Morning star (bullish): bar1 large down, bar2 small and below bar1, bar3 large up
    if c1 < o1 and body2 <= _STAR_BODY_RATIO * body1:
        if max(o2, c2) <= min(o1, c1):   # star below bar1 body
            if c3 > o3 and c3 > midpoint1:
                return "long"

    # Evening star (bearish): bar1 large up, bar2 small and above bar1, bar3 large down
    body1_up = c1 - o1
    if body1_up > 0 and body2 <= _STAR_BODY_RATIO * body1_up:
        if min(o2, c2) >= max(o1, c1):   # star above bar1 body
            midpt = o1 + body1_up / 2.0
            if c3 < o3 and c3 < midpt:
                return "short"

    return None
