#!/usr/bin/env python3
"""rising_falling_three_methods_continuation -- 5-bar bull/bear flag continuation pattern. j_person_a_complete_guide_to_technical_trading_tac.

Rising three methods (bullish): candle1 long up; candles 2-4 small and stay within candle1 range
(inside/inside-ish); candle5 long up closing above candle1 close. Falling three mirrors.
Signal fires at candle5 close (pos = current = candle5).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "rising_falling_three_methods_continuation",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "continuation",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,atr",
    "long": "5-bar rising three methods: large up candle, 3 small inside candles, final large up close above candle1 close",
    "short": "5-bar falling three methods: large down candle, 3 small inside candles, final large down close below candle1 close",
    "desc": "Rising/falling three methods: 5-bar bull/bear flag with inside consolidation then breakout continuation",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}

_LARGE_RATIO  = 0.5    # candle1 and candle5 body must be >= 50% of their range
_SMALL_RATIO  = 0.5    # middle candles body must be <= 50% of candle1 body


def signal(ind, pos, htf=None):
    """Rising/falling three methods: 5-bar continuation flag pattern."""
    if pos < 4:
        return None
    o = ind["open"]
    h = ind["high"]
    lo = ind["low"]
    c = ind["close"]
    atr = ind["atr"][pos]
    if nan(atr) or atr == 0:
        return None
    for k in range(pos-4, pos+1):
        if nan(o[k], h[k], lo[k], c[k]):
            return None

    # --- Rising Three Methods (bullish continuation) ---
    # Candle1 = pos-4: large UP
    body1 = c[pos-4] - o[pos-4]
    rng1  = h[pos-4] - lo[pos-4]
    if body1 > 0 and rng1 > 0 and body1 >= _LARGE_RATIO * rng1:
        # Middle 3 candles (pos-3, pos-2, pos-1): small bodies within candle1 range
        mid_ok = True
        for k in range(pos-3, pos):
            bk = abs(c[k] - o[k])
            if bk > _SMALL_RATIO * body1:
                mid_ok = False
                break
            if h[k] > h[pos-4] or lo[k] < lo[pos-4]:
                mid_ok = False
                break
        if mid_ok:
            # Candle5 = pos: large UP closing above candle1 close
            body5 = c[pos] - o[pos]
            rng5  = h[pos] - lo[pos]
            if (body5 > 0 and rng5 > 0 and
                    body5 >= _LARGE_RATIO * rng5 and
                    c[pos] > c[pos-4]):
                return "long"

    # --- Falling Three Methods (bearish continuation) ---
    # Candle1 = pos-4: large DOWN
    body1d = o[pos-4] - c[pos-4]
    if body1d > 0 and rng1 > 0 and body1d >= _LARGE_RATIO * rng1:
        mid_ok = True
        for k in range(pos-3, pos):
            bk = abs(c[k] - o[k])
            if bk > _SMALL_RATIO * body1d:
                mid_ok = False
                break
            if h[k] > h[pos-4] or lo[k] < lo[pos-4]:
                mid_ok = False
                break
        if mid_ok:
            # Candle5: large DOWN closing below candle1 close
            body5d = o[pos] - c[pos]
            rng5   = h[pos] - lo[pos]
            if (body5d > 0 and rng5 > 0 and
                    body5d >= _LARGE_RATIO * rng5 and
                    c[pos] < c[pos-4]):
                return "short"

    return None
