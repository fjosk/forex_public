#!/usr/bin/env python3
"""pinocchio_pin_bar_strategy -- Pin bar / Pinocchio: long-wick small-body reversal candle. binary_options_trading_strategies_links_secure.

Bearish pin bar: after uptrend, small real body + long upper wick (>=2x body) = selling pressure.
Bullish pin bar: after downtrend, small real body + long lower wick (>=2x body) = buying pressure.
Trend context via EMA50.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pinocchio_pin_bar_strategy",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1h-4h",
    "indicators": "open,high,low,close,ema50",
    "long": "Lower wick >= 2x real body AND prior downtrend (close<ema50); small upper shadow",
    "short": "Upper wick >= 2x real body AND prior uptrend (close>ema50); small lower shadow",
    "desc": "Pinocchio pin bar: tall-shadow small-body single candle reversal with trend filter",
    "source": "book:binary_options_trading_strategies_links_secure",
}

_SHADOW_RATIO = 2.0     # dominant shadow must be >= 2x body
_SMALL_OTHER  = 0.5     # the opposite shadow must be <= 50% of dominant shadow


def signal(ind, pos, htf=None):
    """Pin bar: long wick with small body signals reversal against prior trend."""
    if pos < 1:
        return None
    o   = ind["open"][pos]
    h   = ind["high"][pos]
    lo  = ind["low"][pos]
    c   = ind["close"][pos]
    ema = ind["ema50"][pos]
    if nan(o, h, lo, c, ema):
        return None

    body       = abs(c - o)
    upper_shad = h - max(o, c)
    lower_shad = min(o, c) - lo

    # Bearish pin bar: long upper wick after uptrend
    if c > ema:
        if (upper_shad >= _SHADOW_RATIO * max(body, 1e-10) and
                lower_shad <= _SMALL_OTHER * upper_shad):
            return "short"

    # Bullish pin bar: long lower wick after downtrend
    if c < ema:
        if (lower_shad >= _SHADOW_RATIO * max(body, 1e-10) and
                upper_shad <= _SMALL_OTHER * lower_shad):
            return "long"

    return None
