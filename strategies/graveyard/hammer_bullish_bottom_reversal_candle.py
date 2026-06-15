#!/usr/bin/env python3
"""hammer_bullish_bottom_reversal_candle -- Hammer: lower shadow >= 2x real body, tiny upper
shadow; bullish bottom reversal after a downtrend (close below ema50).
J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'hammer'."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "hammer_bullish_bottom_reversal_candle",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,ema50",
    "long": "hammer at bottom: lower_shadow >= 2*body, tiny upper shadow, close below ema50",
    "short": "none (long-only pattern; see hanging_man for bearish twin)",
    "desc": "Hammer bullish bottom reversal: lower shadow >= twice the body, at a downtrend low",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'hammer'; p.45",
}

_UPPER_SHD_MAX = 0.10   # upper shadow <= 10% of body (tiny)


def signal(ind, pos, htf=None):
    """Hammer long-only reversal at bottoms below ema50."""
    if pos < 1:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    ema = ind["ema50"][pos]
    if nan(o, h, l, c, ema):
        return None
    body = abs(c - o)
    if body <= 0:
        return None
    lower_shadow = min(o, c) - l
    upper_shadow = h - max(o, c)
    # Hammer: lower shadow >= 2x body, upper shadow tiny, in downtrend
    if (lower_shadow >= 2.0 * body and
            upper_shadow <= _UPPER_SHD_MAX * body and
            c < ema):
        return "long"
    return None
