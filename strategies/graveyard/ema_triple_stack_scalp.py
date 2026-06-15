#!/usr/bin/env python3
"""ema_triple_stack_scalp -- EMA stack bounce: candle crosses EMA50 in direction of triple alignment. zeta-zetra."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_triple_stack_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema21, ema50, ema200, open, close, high, low",
    "long": "ema21>ema50>ema200 all sloping up, candle opens below ema50 and closes above it",
    "short": "ema21<ema50<ema200 all sloping down, candle opens above ema50 and closes below it",
    "desc": "Triple EMA stack scalp: EMA50 dynamic bounce entry in aligned-stack direction",
    "source": "https://github.com/zeta-zetra/code",
}

_WICK_LIMIT = 2e-5


def signal(ind, pos, htf=None):
    """Triple EMA stack bounce at EMA50."""
    e21 = ind["ema21"][pos]
    e21_1 = ind["ema21"][pos - 1]
    e50 = ind["ema50"][pos]
    e50_1 = ind["ema50"][pos - 1]
    e200 = ind["ema200"][pos]
    e200_1 = ind["ema200"][pos - 1]
    o = ind["open"][pos]
    c = ind["close"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(e21, e21_1, e50, e50_1, e200, e200_1, o, c, h, lo):
        return None
    bull_stack = e21 > e50 > e200 and e21 > e21_1 and e50 > e50_1 and e200 > e200_1
    bear_stack = e21 < e50 < e200 and e21 < e21_1 and e50 < e50_1 and e200 < e200_1
    if bull_stack and o < e50 and c > e50 and (o - lo) <= _WICK_LIMIT:
        return "long"
    if bear_stack and o > e50 and c < e50 and (h - o) <= _WICK_LIMIT:
        return "short"
    return None
