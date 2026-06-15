#!/usr/bin/env python3
"""tweezers_top_bottom_reversal -- Two-candle equal-extreme reversal pattern. currency_trading_for_dummies_2nd_edition_by_brian.

Tweezers top: two consecutive candles with matching (equal within tolerance) highs + long upper
shadows after an up move. Tweezers bottom: matching lows + long lower shadows after a down move.
Tolerance = ATR fraction. Prior trend via EMA50.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "tweezers_top_bottom_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,atr,ema50",
    "long": "Two consecutive bars with matching lows (within ATR tolerance) AND long lower shadows AND prior downtrend",
    "short": "Two consecutive bars with matching highs (within ATR tolerance) AND long upper shadows AND prior uptrend",
    "desc": "Tweezers top/bottom: two-candle pattern with equal extremes signals failure to extend",
    "source": "book:currency_trading_for_dummies_2nd_edition_by_brian",
}

_MATCH_TOLERANCE = 0.15   # highs/lows match if within 15% of ATR
_SHADOW_RATIO    = 1.5    # dominant shadow >= 1.5x body


def signal(ind, pos, htf=None):
    """Tweezers: two candles with matching extremes + long tails -> reversal."""
    if pos < 2:
        return None
    o   = ind["open"]
    h   = ind["high"]
    lo  = ind["low"]
    c   = ind["close"]
    atr = ind["atr"][pos]
    ema = ind["ema50"][pos]
    if nan(h[pos], lo[pos], c[pos], o[pos],
           h[pos-1], lo[pos-1], c[pos-1], o[pos-1],
           atr, ema) or atr == 0:
        return None

    tol = _MATCH_TOLERANCE * atr

    # Tweezers top: matching highs + long upper shadows + prior uptrend
    if c[pos] > ema:
        highs_match = abs(h[pos] - h[pos-1]) <= tol
        up_shad1 = h[pos-1] - max(o[pos-1], c[pos-1])
        up_shad2 = h[pos]   - max(o[pos],   c[pos])
        body1 = abs(c[pos-1] - o[pos-1])
        body2 = abs(c[pos]   - o[pos])
        if (highs_match and
                up_shad1 >= _SHADOW_RATIO * max(body1, 1e-10) and
                up_shad2 >= _SHADOW_RATIO * max(body2, 1e-10)):
            return "short"

    # Tweezers bottom: matching lows + long lower shadows + prior downtrend
    if c[pos] < ema:
        lows_match = abs(lo[pos] - lo[pos-1]) <= tol
        lo_shad1 = min(o[pos-1], c[pos-1]) - lo[pos-1]
        lo_shad2 = min(o[pos],   c[pos])   - lo[pos]
        body1 = abs(c[pos-1] - o[pos-1])
        body2 = abs(c[pos]   - o[pos])
        if (lows_match and
                lo_shad1 >= _SHADOW_RATIO * max(body1, 1e-10) and
                lo_shad2 >= _SHADOW_RATIO * max(body2, 1e-10)):
            return "long"

    return None
