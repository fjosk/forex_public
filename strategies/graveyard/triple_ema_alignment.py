#!/usr/bin/env python3
"""triple_ema_alignment -- Three-EMA bull/bear stack entry on alignment change. MetaQuotes MQL5 250."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "triple_ema_alignment",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5, ema20, ema50",
    "long": "ema5 > ema20 > ema50 (bull stack) AND not bull stack on prior bar",
    "short": "ema5 < ema20 < ema50 (bear stack) AND not bear stack on prior bar",
    "desc": "Triple EMA alignment (5/20/50): enter on the bar when all three EMAs first stack",
    "source": "MetaQuotes MQL5 Wizard -- Signals Based on Three Moving Averages (MQL5 Code Base 250)",
}


def signal(ind, pos, htf=None):
    """Fire on the bar where the three-EMA stack first forms."""
    f = ind["ema5"][pos]
    m = ind["ema20"][pos]
    s = ind["ema50"][pos]
    f1 = ind["ema5"][pos - 1]
    m1 = ind["ema20"][pos - 1]
    s1 = ind["ema50"][pos - 1]
    if nan(f, m, s, f1, m1, s1):
        return None
    bull_now = f > m > s
    bear_now = f < m < s
    bull_prev = f1 > m1 > s1
    bear_prev = f1 < m1 < s1
    if bull_now and not bull_prev:
        return "long"
    if bear_now and not bear_prev:
        return "short"
    return None
