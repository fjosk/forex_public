#!/usr/bin/env python3
"""rsi_divergence -- RSI regular divergence: price vs RSI N-bar window + RSI zone filter + confirming bar. forextraininggroup.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_divergence",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "rsi, close, open",
    "long": "price lower low AND rsi higher low over 5-bar window; rsi < 40; bullish confirming bar",
    "short": "price higher high AND rsi lower high; rsi > 60; bearish confirming bar",
    "desc": "Classic RSI divergence: price vs RSI over 5-bar window with zone filter and confirming candle",
    "source": "web:https://forextraininggroup.com/an-in-depth-look-at-the-rsi-divergence-strategy/",
}

_LB = 5


def signal(ind, pos, htf=None):
    """RSI divergence with zone filter (rsi<40 bull, rsi>60 bear) and confirming candle."""
    if pos < _LB + 1:
        return None
    c = ind["close"][pos]
    op = ind["open"][pos]
    rs = ind["rsi"][pos]
    if nan(c, op, rs):
        return None

    window_c = ind["close"][pos - _LB:pos]
    window_rs = ind["rsi"][pos - _LB:pos]
    if any(nan(v) for v in window_c) or any(nan(v) for v in window_rs):
        return None

    import numpy as np
    lo_c = float(np.min(window_c))
    hi_c = float(np.max(window_c))
    lo_rs = float(np.min(window_rs))
    hi_rs = float(np.max(window_rs))

    bull_div = c < lo_c and rs > lo_rs and rs < 40
    bear_div = c > hi_c and rs < hi_rs and rs > 60
    bull_bar = c > op
    bear_bar = c < op

    if bull_div and bull_bar:
        return "long"
    if bear_div and bear_bar:
        return "short"
    return None
