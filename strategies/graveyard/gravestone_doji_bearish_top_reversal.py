#!/usr/bin/env python3
"""gravestone_doji_bearish_top_reversal -- Gravestone doji: open and close near the session
low, long upper shadow; bearish top signal above ema20.
J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'gravestone doji'."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "gravestone_doji_bearish_top_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,ema20",
    "long": "none (short-only pattern)",
    "short": "open~close~low (near-zero lower shadow), large upper shadow; close above ema20",
    "desc": "Gravestone doji bearish top reversal: open and close at session low, long upper wick",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'gravestone doji'",
}

_BODY_RATIO = 0.08      # body <= 8% of range = doji
_LOWER_SHD_MAX = 0.10   # lower shadow <= 10% of range (flat bottom)
_UPPER_SHD_MIN = 0.60   # upper shadow >= 60% of range (long upper wick)


def signal(ind, pos, htf=None):
    """Gravestone doji short-only reversal at tops above ema20."""
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
    lower_shadow = min(o, c) - l
    upper_shadow = h - max(o, c)
    # Gravestone geometry: tiny body, flat bottom, long upper wick
    if (body <= _BODY_RATIO * rng and
            lower_shadow <= _LOWER_SHD_MAX * rng and
            upper_shadow >= _UPPER_SHD_MIN * rng and
            c > ema):
        return "short"
    return None
