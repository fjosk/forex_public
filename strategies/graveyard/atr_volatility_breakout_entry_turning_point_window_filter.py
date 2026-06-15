#!/usr/bin/env python3
"""atr_volatility_breakout_from_close -- Price moves 1.5x ATR from prior close triggers entry. trade_your_way_to_financial_freedom."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "atr_volatility_breakout_entry_turning_point_window_filter",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "atr, close, high, low",
    "long": "high >= prev_close + 1.5 * ATR",
    "short": "low <= prev_close - 1.5 * ATR",
    "desc": "ATR volatility breakout: 1.5x ATR move from prior close signals directional breakout",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp",
}


def signal(ind, pos, htf=None):
    """Breakout when price moves 1.5x ATR from prior bar close."""
    if pos < 2:
        return None
    a = ind["atr"][pos]
    prev_c = ind["close"][pos - 1]
    h = ind["high"][pos]
    l = ind["low"][pos]
    if nan(a, prev_c, h, l) or a <= 0:
        return None
    trigger = 1.5 * a
    if h >= prev_c + trigger:
        return "long"
    if l <= prev_c - trigger:
        return "short"
    return None
