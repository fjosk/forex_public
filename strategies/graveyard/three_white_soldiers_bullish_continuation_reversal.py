#!/usr/bin/env python3
"""three_white_soldiers_bullish_continuation_reversal -- Three white soldiers: 3 consecutive up candles near highs. j_person_a_complete_guide_to_technical_trading_tac.

Three white soldiers: three consecutive up candles (close>open) each closing at or near their
high. Reliable after consolidation at a bottom or early in an uptrend. Bullish signal only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "three_white_soldiers_bullish_continuation_reversal",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h-1d",
    "indicators": "open,high,low,close",
    "long": "Three consecutive up candles (close>open) each closing near their high and closing higher than prior",
    "short": "none (three white soldiers is long-only)",
    "desc": "Three white soldiers: 3-bar bullish momentum pattern with closes near each bar's high",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}

_CLOSE_NEAR_HIGH = 0.25   # (high - close) <= 25% of bar range


def signal(ind, pos, htf=None):
    """Three white soldiers: 3 up closes near highs."""
    if pos < 3:
        return None
    o = ind["open"]
    h = ind["high"]
    lo = ind["low"]
    c = ind["close"]
    for k in range(pos-2, pos+1):
        if nan(o[k], h[k], lo[k], c[k]):
            return None

    for k in range(pos-2, pos+1):
        rng = h[k] - lo[k]
        # Must be up candle
        if c[k] <= o[k]:
            return None
        # Close must be near high
        if rng > 0 and (h[k] - c[k]) > _CLOSE_NEAR_HIGH * rng:
            return None
        # Closes must be rising
        if k > pos-2 and c[k] <= c[k-1]:
            return None

    return "long"
