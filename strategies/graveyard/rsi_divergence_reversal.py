#!/usr/bin/env python3
"""rsi_divergence_reversal -- RSI divergence via N-bar window; EMA9 confirmation cross. forextraininggroup.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_divergence_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "rsi, ema9, close, low, high",
    "long": "Bullish div: low < 10-bar window low AND rsi > 10-bar window rsi-low; confirmed by close > ema9",
    "short": "Bearish div: high > 10-bar window high AND rsi < 10-bar window rsi-high; confirmed by close < ema9",
    "desc": "RSI divergence reversal: N-bar price vs RSI divergence with EMA9 confirmation",
    "source": "web:https://forextraininggroup.com/an-in-depth-look-at-the-rsi-divergence-strategy/",
}

_LB = 10


def signal(ind, pos, htf=None):
    """RSI divergence over N-bar window confirmed by EMA9 crossover."""
    if pos < _LB + 1:
        return None
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    rs = ind["rsi"][pos]
    c = ind["close"][pos]
    e9 = ind["ema9"][pos]
    e9p = ind["ema9"][pos - 1]
    cp = ind["close"][pos - 1]
    if nan(lo, hi, rs, c, e9, e9p, cp):
        return None

    window_lo = ind["low"][pos - _LB:pos]
    window_hi = ind["high"][pos - _LB:pos]
    window_rs = ind["rsi"][pos - _LB:pos]
    if any(nan(v) for v in window_lo) or any(nan(v) for v in window_rs):
        return None

    import numpy as np
    w_lo = float(np.min(window_lo))
    w_hi = float(np.max(window_hi))
    w_rs_lo = float(np.min(window_rs))
    w_rs_hi = float(np.max(window_rs))

    bull_div = lo < w_lo and rs > w_rs_lo and rs < 40
    bear_div = hi > w_hi and rs < w_rs_hi and rs > 60

    ema9_bull = c > e9 and cp <= e9p
    ema9_bear = c < e9 and cp >= e9p

    if bull_div and ema9_bull:
        return "long"
    if bear_div and ema9_bear:
        return "short"
    return None
