#!/usr/bin/env python3
"""hammer_hanging_man -- Hammer (after downtrend) or hanging man (after uptrend): lower shadow
>= 2x body, tiny upper shadow; ema20 for trend direction.
J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.45."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "hammer_hanging_man",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,ema20",
    "long": "hammer after downtrend: lower shadow >= 2x body, tiny upper shadow, close below ema20",
    "short": "hanging man after uptrend: same geometry, close above ema20",
    "desc": "Hammer/hanging man: long lower tail reversal at bottom (long) or top (short)",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.45",
}

_UPPER_SHD_MAX_RATIO = 0.10  # upper shadow <= 10% of range


def signal(ind, pos, htf=None):
    """Hammer (long) or hanging man (short) based on trend context."""
    if pos < 1:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    ema = ind["ema20"][pos]
    if nan(o, h, l, c, ema):
        return None
    rng = h - l
    if rng <= 0:
        return None
    body = abs(c - o)
    if body <= 0:
        return None
    lower_shadow = min(o, c) - l
    upper_shadow = h - max(o, c)
    # Geometry: lower shadow >= 2x body, upper shadow <= 10% of range
    if lower_shadow < 2.0 * body:
        return None
    if upper_shadow > _UPPER_SHD_MAX_RATIO * rng:
        return None
    # Direction by trend
    if c < ema:
        return "long"   # hammer in downtrend
    if c > ema:
        return "short"  # hanging man in uptrend
    return None
