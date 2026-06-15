#!/usr/bin/env python3
"""shooting_star_bearish_top_reversal_candle -- Shooting star: long upper shadow at top. j_person_a_complete_guide_to_technical_trading_tac.

Shooting star: upper shadow >= 2x real body, little/no lower shadow, body near session low.
Appears after an advance. Bearish reversal signal. Trend context via EMA50.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "shooting_star_bearish_top_reversal_candle",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1h-4h",
    "indicators": "open,high,low,close,ema50",
    "long": "none (shooting star is short-only)",
    "short": "Upper shadow >= 2x body AND lower shadow near zero AND body near session low AND prior uptrend",
    "desc": "Shooting star: tall upper wick single candle at top of advance signals bearish reversal",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}

_SHADOW_RATIO = 2.0    # upper shadow >= 2x body
_LOWER_MAX    = 0.25   # lower shadow <= 25% of upper shadow


def signal(ind, pos, htf=None):
    """Shooting star: long upper shadow at top signals bearish reversal."""
    if pos < 1:
        return None
    o   = ind["open"][pos]
    h   = ind["high"][pos]
    lo  = ind["low"][pos]
    c   = ind["close"][pos]
    ema = ind["ema50"][pos]
    if nan(o, h, lo, c, ema):
        return None

    # Require prior uptrend
    if c <= ema:
        return None

    body       = abs(c - o)
    upper_shad = h - max(o, c)
    lower_shad = min(o, c) - lo

    if (upper_shad >= _SHADOW_RATIO * max(body, 1e-10) and
            lower_shad <= _LOWER_MAX * upper_shad):
        return "short"

    return None
