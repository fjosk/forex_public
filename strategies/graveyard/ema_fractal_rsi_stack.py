#!/usr/bin/env python3
"""ema_fractal_rsi_stack -- EMA Stack + RSI + Fractal Confirmation (zeta-zetra).
web:https://github.com/zeta-zetra/code
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_fractal_rsi_stack",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "ema21, ema50, ema200, rsi, frac_up, frac_dn",
    "long": "ema21>ema50>ema200 (all slopes positive) AND rsi>50 AND frac_up>0 AND close above all EMAs",
    "short": "ema21<ema50<ema200 (all slopes negative) AND rsi<50 AND frac_dn>0 AND close below all EMAs",
    "desc": "Multi-filter trend: bullish EMA stack with positive slopes + RSI + fractal + price position",
    "source": "web:https://github.com/zeta-zetra/code",
}


def signal(ind, pos, htf=None):
    """Bullish/bearish EMA stack with slope confirmation, RSI midline, and fractal signal."""
    e21 = ind["ema21"][pos]
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    e21_1 = ind["ema21"][pos - 1]
    e50_1 = ind["ema50"][pos - 1]
    e200_1 = ind["ema200"][pos - 1]
    rs = ind["rsi"][pos]
    fu = ind["frac_up"][pos]
    fd = ind["frac_dn"][pos]
    c = ind["close"][pos]
    if nan(e21, e50, e200, e21_1, e50_1, e200_1, rs, fu, fd, c):
        return None
    bullish_stack = e21 > e50 > e200
    bearish_stack = e21 < e50 < e200
    all_rising = e21 > e21_1 and e50 > e50_1 and e200 > e200_1
    all_falling = e21 < e21_1 and e50 < e50_1 and e200 < e200_1
    if bullish_stack and all_rising and rs > 50 and fu > 0 and c > e21 and c > e50 and c > e200:
        return "long"
    if bearish_stack and all_falling and rs < 50 and fd > 0 and c < e21 and c < e50 and c < e200:
        return "short"
    return None
