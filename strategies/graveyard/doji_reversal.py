#!/usr/bin/env python3
"""doji_reversal -- Doji reversal: gravestone doji (open~close~low, long upper wick) is short;
dragonfly doji (open~close~high, long lower wick) is long. Trend context via ema20.
J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.46."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "doji_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,ema20",
    "long": "dragonfly doji: open~close near high, long lower wick; close below ema20 (downtrend bottom)",
    "short": "gravestone doji: open~close near low, long upper wick; close above ema20 (uptrend top)",
    "desc": "Gravestone/dragonfly doji reversal filtered by ema20 trend context",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.46",
}

_BODY_RATIO = 0.08    # body <= 8% of range = doji
_SHADOW_RATIO = 0.80  # the dominant shadow covers >= 80% of range


def signal(ind, pos, htf=None):
    """Gravestone doji -> short; dragonfly doji -> long; both gated by ema20."""
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
    if body > _BODY_RATIO * rng:
        return None
    upper_shadow = h - max(o, c)
    lower_shadow = min(o, c) - l
    # Dragonfly: long lower shadow, tiny upper shadow -> at bottom -> long
    if lower_shadow >= _SHADOW_RATIO * rng and upper_shadow <= 0.1 * rng and c < ema:
        return "long"
    # Gravestone: long upper shadow, tiny lower shadow -> at top -> short
    if upper_shadow >= _SHADOW_RATIO * rng and lower_shadow <= 0.1 * rng and c > ema:
        return "short"
    return None
