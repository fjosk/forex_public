#!/usr/bin/env python3
"""rsi_divergence_swing -- RSI divergence swing: N-bar price/RSI divergence + reversal bar confirmation. ForexFactory."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_divergence_swing",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "rsi, close, open, low, high",
    "long": "price lower low over 5 bars AND rsi not at new low (higher low); close > open confirmation",
    "short": "price higher high over 5 bars AND rsi not at new high (lower high); close < open confirmation",
    "desc": "RSI divergence swing: 5-bar price vs RSI divergence + bullish/bearish bar confirmation",
    "source": "web:https://www.forexfactory.com/thread/145290-rsi-divergence",
}

_LB = 5


def signal(ind, pos, htf=None):
    """RSI divergence via 5-bar window comparison + confirming candle direction."""
    if pos < _LB + 1:
        return None
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    c = ind["close"][pos]
    op = ind["open"][pos]
    rs = ind["rsi"][pos]
    if nan(lo, hi, c, op, rs):
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

    price_ll = lo < w_lo
    rsi_hl = rs > w_rs_lo
    bull_div = price_ll and rsi_hl
    bull_bar = c > op and c > ind["close"][pos - 1]

    price_hh = hi > w_hi
    rsi_lh = rs < w_rs_hi
    bear_div = price_hh and rsi_lh
    bear_bar = c < op and c < ind["close"][pos - 1]

    if bull_div and bull_bar:
        return "long"
    if bear_div and bear_bar:
        return "short"
    return None
