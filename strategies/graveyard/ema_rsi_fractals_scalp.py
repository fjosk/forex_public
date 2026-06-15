#!/usr/bin/env python3
"""ema_rsi_fractals_scalp -- EMA Triple Stack + RSI + Fractals Scalp. zeta-zetra/YouTube.

Three-EMA bullish alignment (ema21 > ema50 > ema200), RSI > 50, close above all three,
plus confirmed Williams Fractal up (frac_up at pos-2). Full mirror for short.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_rsi_fractals_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "5m",
    "indicators": "ema21, ema50, ema200, rsi, frac_up, frac_dn, close",
    "long": "ema21>ema50>ema200, close>all EMAs, rsi>50, confirmed bullish fractal at pos-2",
    "short": "ema21<ema50<ema200, close<all EMAs, rsi<50, confirmed bearish fractal at pos-2",
    "desc": "EMA triple stack + RSI midline + Williams Fractal confirmation scalp",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/youtube/ema_rsi_fractals.html",
}


def signal(ind, pos, htf=None):
    """EMA triple stack + RSI + confirmed Williams Fractal."""
    e21 = ind["ema21"][pos]
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    r = ind["rsi"][pos]
    c = ind["close"][pos]
    # Williams fractal at pos-2 (confirmed, not forward-looking)
    fu2 = ind["frac_up"][pos - 2]
    fd2 = ind["frac_dn"][pos - 2]
    if nan(e21, e50, e200, r, c, fu2, fd2):
        return None
    bull_stack = e21 > e50 > e200
    bear_stack = e21 < e50 < e200
    above_all = c > e21 and c > e50 and c > e200
    below_all = c < e21 and c < e50 and c < e200
    if bull_stack and above_all and r > 50 and fu2 != 0:
        return "long"
    if bear_stack and below_all and r < 50 and fd2 != 0:
        return "short"
    return None
