#!/usr/bin/env python3
"""bollinger_atr_range_keltner_squeeze -- BB inside KC squeeze with RSI direction filter. Nikhil-Adithyan.

Squeeze fires when BB was inside Keltner channel on the previous bar but the current bar's BB
expands back outside. RSI > 50 for long, RSI < 50 for short.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bollinger_atr_range_keltner_squeeze",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "bb_up, bb_lo, kc_up, kc_lo, rsi",
    "long": "squeeze fires upward (bb_up crosses above kc_up) AND RSI > 50",
    "short": "squeeze fires downward (bb_lo crosses below kc_lo) AND RSI < 50",
    "desc": "BB-KC squeeze with RSI momentum filter: enter breakout direction confirmed by RSI bias",
    "source": "https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python (BB_KC_RSI)",
}


def signal(ind, pos, htf=None):
    """BB-KC squeeze fire with RSI direction filter."""
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    bb_up1 = ind["bb_up"][pos - 1]
    bb_lo1 = ind["bb_lo"][pos - 1]
    kc_up1 = ind["kc_up"][pos - 1]
    kc_lo1 = ind["kc_lo"][pos - 1]
    rsi = ind["rsi"][pos]
    if nan(bb_up, bb_lo, kc_up, kc_lo, bb_up1, bb_lo1, kc_up1, kc_lo1, rsi):
        return None
    # Previous bar must have been in squeeze
    was_squeeze = (bb_lo1 > kc_lo1) and (bb_up1 < kc_up1)
    if not was_squeeze:
        return None
    # Long: upper band now expands above KC upper and RSI bullish
    if bb_up >= kc_up and rsi > 50:
        return "long"
    # Short: lower band now expands below KC lower and RSI bearish
    if bb_lo <= kc_lo and rsi < 50:
        return "short"
    return None
