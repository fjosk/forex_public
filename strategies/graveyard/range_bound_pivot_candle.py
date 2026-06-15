#!/usr/bin/env python3
"""range_bound_pivot_candle -- Pivot S2/R2 touch + bullish/bearish engulfing or harami. Zeta-zetra.

Mean-reversion at second pivot level confirmed by a candlestick reversal pattern.
Long: low < piv_s2 AND bullish engulfing or bullish harami.
Short: high > piv_r2 AND bearish engulfing or bearish harami.
Pattern math is pure OHLC.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "range_bound_pivot_candle",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "piv_r2, piv_s2, open, high, low, close",
    "long": "low < piv_s2 AND bullish engulfing or bullish harami",
    "short": "high > piv_r2 AND bearish engulfing or bearish harami",
    "desc": "Range-bound pivot S2/R2 touch with candlestick reversal confirmation",
    "source": "web:https://github.com/zeta-zetra/code",
}


def signal(ind, pos, htf=None):
    """Pivot S2/R2 touch with reversal candle confirmation."""
    r2 = ind["piv_r2"][pos]
    s2 = ind["piv_s2"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    if nan(r2, s2, h, lo, c, o, c1, o1):
        return None
    # Bullish engulfing: prior bearish, current bullish, current body engulfs prior
    bull_engulf = (c1 < o1) and (c > o) and (o < c1) and (c > o1)
    # Bullish harami: prior bearish, current bullish, current body inside prior
    bull_harami = (c1 < o1) and (c > o) and (c < o1) and (o > c1)
    # Bearish engulfing: prior bullish, current bearish, current body engulfs prior
    bear_engulf = (c1 > o1) and (c < o) and (o > c1) and (c < o1)
    # Bearish harami: prior bullish, current bearish, current body inside prior
    bear_harami = (c1 > o1) and (c < o) and (c > o1) and (o < c1)
    if lo < s2 and (bull_engulf or bull_harami):
        return "long"
    if h > r2 and (bear_engulf or bear_harami):
        return "short"
    return None
