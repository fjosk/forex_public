#!/usr/bin/env python3
"""momentum_breakout_20day_high -- 20-bar high close breakout with MACD/low exit. ForexTester."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "momentum_breakout_20day_high",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "daily",
    "indicators": "hh_n, ll_n, macd, close",
    "long": "close equals or exceeds the 20-bar rolling high (new 20-day high close)",
    "short": "not part of original (long-only system; short added as mirror for FX)",
    "desc": "20-day high momentum breakout: buy new 20-bar high close, ATR trailing stop",
    "source": "web:https://forextester.com/blog/momentum-trading-strategies/",
}


def signal(ind, pos, htf=None):
    """Buy new 20-bar closing high; short mirror on new 20-bar closing low."""
    if pos < 20:
        return None
    c = ind["close"][pos]
    macd = ind["macd"][pos]
    if nan(c, macd):
        return None

    # Compute rolling 20-bar high and low from close array
    closes = [ind["close"][pos - i] for i in range(1, 21)]
    if any(nan(v) for v in closes):
        return None
    high20 = max(closes)
    low20 = min(closes)

    if c > high20 and macd > 0:
        return "long"
    if c < low20 and macd < 0:
        return "short"

    return None
