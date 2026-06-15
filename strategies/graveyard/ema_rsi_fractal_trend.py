#!/usr/bin/env python3
"""ema_rsi_fractal_trend -- EMA triple alignment + RSI > 50 + confirmed Williams fractal. zeta-zetra."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_rsi_fractal_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema21, ema50, ema200, rsi, frac_up, frac_dn",
    "long": "ema21>ema50>ema200 AND rsi>50 AND frac_up confirmed AND close>ema200",
    "short": "ema21<ema50<ema200 AND rsi<50 AND frac_dn confirmed AND close<ema200",
    "desc": "EMA triple alignment + RSI filter + Williams fractal confirmation",
    "source": "https://zeta-zetra.github.io/docs-forex-strategies-python/youtube/ema_rsi_fractals.html",
}


def signal(ind, pos, htf=None):
    """EMA triple alignment + RSI + fractal trend signal."""
    e21 = ind["ema21"][pos]
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    r = ind["rsi"][pos]
    c = ind["close"][pos]
    fu = ind["frac_up"][pos - 2] if pos >= 2 else float("nan")
    fd = ind["frac_dn"][pos - 2] if pos >= 2 else float("nan")
    if nan(e21, e50, e200, r, c):
        return None
    if e21 > e50 and e50 > e200 and r > 50 and not nan(fu) and fu and c > e200:
        return "long"
    if e21 < e50 and e50 < e200 and r < 50 and not nan(fd) and fd and c < e200:
        return "short"
    return None
