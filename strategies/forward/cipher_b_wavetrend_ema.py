#!/usr/bin/env python3
"""cipher_b_wavetrend_ema -- Cipher B: WaveTrend oversold cross + EMA stack + RSI-MFI bias. benso87/Pine.

WaveTrend crosses up while oversold, in bullish EMA stack (close > EMA50 > EMA200),
with RSI-MFI composite positive. Short mirror for bearish stack.
mfi key absent from engine; approximated with rsi alone (RSI-MFI proxy).
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "cipher_b_wavetrend_ema",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h",
    "indicators": "ema50, ema200, wt1, wt2, rsi",
    "long": "close > EMA50 > EMA200 AND wt1 crosses above wt2 from below 0 AND RSI < 50 (oversold bias)",
    "short": "close < EMA50 < EMA200 AND wt1 crosses below wt2 from above 0 AND RSI > 50",
    "desc": "Cipher B WaveTrend oversold cross in EMA bullish/bearish stack",
    "source": "https://github.com/benso87/Private-Pine-Scripts Cipher B strategy.pine",
}


def signal(ind, pos, htf=None):
    """WaveTrend oversold/overbought cross inside EMA stack with RSI bias."""
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    w1 = ind["wt1"][pos]
    w11 = ind["wt1"][pos - 1]
    w2 = ind["wt2"][pos]
    w21 = ind["wt2"][pos - 1]
    r = ind["rsi"][pos]
    if nan(c, e50, e200, w1, w11, w2, w21, r):
        return None
    stack_long = c > e50 and e50 > e200
    stack_short = c < e50 and e50 < e200
    wt_up = _xup(w1, w11, w2, w21) and w2 < 0
    wt_dn = _xdn(w1, w11, w2, w21) and w2 > 0
    if stack_long and wt_up and r < 50:
        return "long"
    if stack_short and wt_dn and r > 50:
        return "short"
    return None
