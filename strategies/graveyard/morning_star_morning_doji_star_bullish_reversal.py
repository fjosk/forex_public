#!/usr/bin/env python3
"""morning_star_morning_doji_star_bullish_reversal -- 3-candle bullish bottom reversal. j_person_a_complete_guide_to_technical_trading_tac.

Morning Star: candle1 large down body; candle2 small body / doji gapping (or simply small relative
to candle1) at the low zone; candle3 large up body closing well into candle1's body (above midpoint).
On FX, true gaps are rare so the 'gap' requirement is relaxed to: candle2 body is small and sits
below the candle1 body midpoint. Signal fires on close of candle3 (pos=current).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "morning_star_morning_doji_star_bullish_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,atr",
    "long": "Candle-3 close above midpoint of candle-1 body; candle-2 small body near bottom; candle-1 large down candle; prior downtrend",
    "short": "none (morning star is long-only; no mirrored evening star here)",
    "desc": "Morning star / morning doji star: three-candle bullish reversal at a bottom",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}

_SMALL_RATIO = 0.35   # candle2 body <= 35% of candle1 body to qualify as small/doji
_LARGE_RATIO = 0.5    # candle1 and candle3 body must be at least 50% of their bar range


def signal(ind, pos, htf=None):
    """Morning star: 3-bar bullish reversal pattern."""
    if pos < 3:
        return None
    o = ind["open"]
    h = ind["high"]
    lo = ind["low"]
    c = ind["close"]
    atr = ind["atr"][pos]
    if nan(o[pos], c[pos], o[pos-1], c[pos-1], o[pos-2], c[pos-2], atr) or atr == 0:
        return None

    # Candle designations: c1=pos-2, c2=pos-1, c3=pos
    # Candle 1: large DOWN candle
    body1 = o[pos-2] - c[pos-2]             # positive when down
    rng1  = h[pos-2] - lo[pos-2]
    if body1 <= 0 or rng1 == 0:
        return None
    if body1 < _LARGE_RATIO * rng1:
        return None                          # candle1 not large enough

    # Candle 2: small body (doji-like), sits below candle1 body midpoint
    body2 = abs(c[pos-1] - o[pos-1])
    mid1  = (o[pos-2] + c[pos-2]) / 2.0
    if body2 > _SMALL_RATIO * body1:
        return None                          # candle2 body too large
    if max(o[pos-1], c[pos-1]) > mid1:
        return None                          # candle2 not low enough

    # Candle 3: large UP candle closing above candle1 midpoint
    body3 = c[pos] - o[pos]                 # positive when up
    rng3  = h[pos] - lo[pos]
    if body3 <= 0 or rng3 == 0:
        return None
    if body3 < _LARGE_RATIO * rng3:
        return None                          # candle3 not large enough
    if c[pos] <= mid1:
        return None                          # close must pierce above candle1 midpoint

    return "long"
