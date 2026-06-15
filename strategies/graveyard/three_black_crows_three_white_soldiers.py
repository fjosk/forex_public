#!/usr/bin/env python3
"""three_black_crows_three_white_soldiers -- Bidirectional 3-bar same-color continuation/reversal. j_person_a_complete_guide_to_technical_trading_tac.

Three white soldiers: three consecutive up candles, each closing higher than the prior close and
near its high. Three black crows: three consecutive down candles, each closing lower with close
near low. Both patterns imply strong momentum; white soldiers = bullish; black crows = bearish.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "three_black_crows_three_white_soldiers",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h-1d",
    "indicators": "open,high,low,close",
    "long": "Three white soldiers: 3 consecutive up candles each closing higher AND near high",
    "short": "Three black crows: 3 consecutive down candles each closing lower AND near low",
    "desc": "Three black crows / three white soldiers: 3-bar directional momentum pattern",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}

_CLOSE_NEAR_EXTREME = 0.25   # close within 25% of bar range from extreme end


def signal(ind, pos, htf=None):
    """Three crows / three soldiers: 3-bar same-direction momentum pattern."""
    if pos < 3:
        return None
    o = ind["open"]
    h = ind["high"]
    lo = ind["low"]
    c = ind["close"]
    for k in range(pos-2, pos+1):
        if nan(o[k], h[k], lo[k], c[k]):
            return None

    # Three white soldiers: each bar up, closing higher, near high
    soldiers = True
    for k in range(pos-2, pos+1):
        rng = h[k] - lo[k]
        if c[k] <= o[k]:
            soldiers = False
            break
        if k > pos-2 and c[k] <= c[k-1]:
            soldiers = False
            break
        if rng > 0 and (h[k] - c[k]) > _CLOSE_NEAR_EXTREME * rng:
            soldiers = False
            break

    if soldiers:
        return "long"

    # Three black crows: each bar down, closing lower, near low
    crows = True
    for k in range(pos-2, pos+1):
        rng = h[k] - lo[k]
        if c[k] >= o[k]:
            crows = False
            break
        if k > pos-2 and c[k] >= c[k-1]:
            crows = False
            break
        if rng > 0 and (c[k] - lo[k]) > _CLOSE_NEAR_EXTREME * rng:
            crows = False
            break

    if crows:
        return "short"

    return None
