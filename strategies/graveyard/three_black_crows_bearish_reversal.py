#!/usr/bin/env python3
"""three_black_crows_bearish_reversal -- Three consecutive down candles closing near lows after advance. j_person_a_complete_guide_to_technical_trading_tac.

Three black crows: three consecutive dark (down) candles that each close on or near their lows,
following an extended advance. Each candle: close < open AND (close - low) is small relative to
bar range (close near low). Prior uptrend via EMA50. Bearish reversal signal.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "three_black_crows_bearish_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,ema50",
    "long": "none (three black crows is short-only)",
    "short": "Three consecutive down candles (close<open) each closing near their low; prior uptrend (close>ema50)",
    "desc": "Three black crows: three consecutive down-close candles near their lows after an uptrend",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}

_CLOSE_NEAR_LOW = 0.25   # (close - low) <= 25% of bar range = closing near low


def signal(ind, pos, htf=None):
    """Three black crows: 3 consecutive down candles closing near lows after advance."""
    if pos < 3:
        return None
    o   = ind["open"]
    h   = ind["high"]
    lo  = ind["low"]
    c   = ind["close"]
    ema = ind["ema50"][pos]
    if nan(ema):
        return None
    for k in range(pos-2, pos+1):
        if nan(o[k], h[k], lo[k], c[k]):
            return None

    # Prior uptrend
    if c[pos-3] <= ema:
        return None

    for k in range(pos-2, pos+1):
        # Each candle must be down
        if c[k] >= o[k]:
            return None
        # Each must close near its low
        rng = h[k] - lo[k]
        if rng > 0 and (c[k] - lo[k]) > _CLOSE_NEAR_LOW * rng:
            return None

    return "short"
