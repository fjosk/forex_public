#!/usr/bin/env python3
"""rsi_divergence_structure_confirm -- RSI divergence with RSI 50 reclaim/break structural confirmation. ebc.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_divergence_structure_confirm",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "rsi, atr, low, high",
    "long": "Bullish div (low lower low, rsi higher low) confirmed by RSI crossing above 50",
    "short": "Bearish div (high higher high, rsi lower high) confirmed by RSI crossing below 50",
    "desc": "RSI divergence + structural confirmation via RSI 50 reclaim or break",
    "source": "web:https://www.ebc.com/forex/rsi-divergence-strategies-timing-the-market-like-a-pro",
}

_LB = 10


def signal(ind, pos, htf=None):
    """RSI divergence over N bars with RSI 50 cross as structural confirmation."""
    if pos < _LB + 1:
        return None
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    rs = ind["rsi"][pos]
    rsp = ind["rsi"][pos - 1]
    if nan(lo, hi, rs, rsp):
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

    bull_div = lo < w_lo and rs > w_rs_lo
    bear_div = hi > w_hi and rs < w_rs_hi

    rsi_cross_up = rs > 50 and rsp <= 50
    rsi_cross_dn = rs < 50 and rsp >= 50

    if bull_div and rsi_cross_up:
        return "long"
    if bear_div and rsi_cross_dn:
        return "short"
    return None
