#!/usr/bin/env python3
"""piercing_pattern_bullish_two_candle_reversal -- Two-candle bullish reversal at bottom. j_person_a_complete_guide_to_technical_trading_tac.

Candle1: long dark (down) candle. Candle2 (current): opens below candle1 low AND closes more than
halfway into candle1 real body (above midpoint), but still below candle1 open. Prior downtrend
confirmed via close below ema50. Classic piercing line pattern.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "piercing_pattern_bullish_two_candle_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,ema50",
    "long": "Candle1 long down body; candle2 opens below candle1 low, closes above candle1 body midpoint; prior downtrend",
    "short": "none (piercing pattern is long-only; dark cloud cover is a separate pattern)",
    "desc": "Piercing pattern: two-candle bullish reversal where the up-candle closes into the prior down-candle body",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}

_LARGE_BODY_RATIO = 0.5   # candle1 body must be >= 50% of bar range


def signal(ind, pos, htf=None):
    """Piercing pattern: bullish 2-bar reversal at a bottom."""
    if pos < 2:
        return None
    o   = ind["open"]
    lo  = ind["low"]
    c   = ind["close"]
    h   = ind["high"]
    ema = ind["ema50"][pos]
    if nan(o[pos], lo[pos], c[pos], h[pos],
           o[pos-1], lo[pos-1], c[pos-1], h[pos-1], ema):
        return None

    # Prior downtrend
    if c[pos] >= ema:
        return None

    # Candle 1: long DOWN candle
    body1 = o[pos-1] - c[pos-1]        # positive = down candle
    rng1  = h[pos-1] - lo[pos-1]
    if body1 <= 0 or rng1 == 0:
        return None
    if body1 < _LARGE_BODY_RATIO * rng1:
        return None                     # not a large down candle

    # Candle 2 conditions
    mid1 = (o[pos-1] + c[pos-1]) / 2.0
    if o[pos] >= lo[pos-1]:
        return None                     # must open below candle1 low
    if c[pos] <= mid1:
        return None                     # must close above candle1 midpoint
    if c[pos] >= o[pos-1]:
        return None                     # must not exceed candle1 open (else full engulfing)
    if c[pos] <= o[pos]:
        return None                     # candle2 must be up (close > open)

    return "long"
