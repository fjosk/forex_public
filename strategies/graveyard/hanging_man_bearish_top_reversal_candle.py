#!/usr/bin/env python3
"""hanging_man_bearish_top_reversal_candle -- Hanging man: same geometry as hammer (lower
shadow >= 2x body, tiny upper shadow) but at a market top after an uptrend.
J. Person, A Complete Guide to Technical Trading Tactics, Glossary; Index p.45, 57."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "hanging_man_bearish_top_reversal_candle",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,ema50",
    "long": "none (short-only pattern)",
    "short": "hanging man at top: lower_shadow >= 2*body, tiny upper shadow, close above ema50",
    "desc": "Hanging man bearish top reversal candle: hammer geometry after uptrend",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'hammer' / 'hanging man'; p.45, 57",
}

_UPPER_SHD_MAX = 0.10   # upper shadow <= 10% of body (tiny)


def signal(ind, pos, htf=None):
    """Hanging man short-only reversal at tops above ema50."""
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
    # Hanging man geometry: lower shadow >= 2x body, upper shadow tiny; in uptrend
    if (lower_shadow >= 2.0 * body and
            upper_shadow <= _UPPER_SHD_MAX * body and
            c > ema):
        return "short"
    return None
