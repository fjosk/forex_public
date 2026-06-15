#!/usr/bin/env python3
"""engulfing_trend -- Engulfing reversal, trend-filtered.. Ported from sister-lab catalog (https://www.investopedia.com/terms/b/bullishengulfingpattern.asp).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "engulfing_trend", "cadences": ['day', 'swing'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "pattern", "tf": "1h-4h", "indicators": "Engulfing candles, EMA50",
    "long": "Bullish engulfing with close>EMA50", "short": "Bearish engulfing with close<EMA50", "desc": "Engulfing reversal, trend-filtered.", "source": "sister-lab catalog: https://www.investopedia.com/terms/b/bullishengulfingpattern.asp",
}


def signal(I, i, htf):
    o, c, o1, c1, e50 = I["open"][i], I["close"][i], I["open"][i-1], I["close"][i-1], I["ema50"][i]
    if _nan(o, c, o1, c1, e50):
        return None
    bull = c1 < o1 and c > o and c >= o1 and o <= c1
    bear = c1 > o1 and c < o and c <= o1 and o >= c1
    if bull and e50 == e50 and c > e50:
        return "long"
    if bear and c < e50:
        return "short"
    return None
