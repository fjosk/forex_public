#!/usr/bin/env python3
"""volatility_breakout_atr_range_expansion -- Volatility Breakout (ATR Range Expansion): buy/sell when price moves at least 0.8 x ATR from the prior close in a single bar; intrabar high/low touch used to detect the threshold crossing. Tharp Ch.8.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "volatility_breakout_atr_range_expansion",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "atr, high, low, close",
    "long": "High reaches prev_close + 0.8*ATR (upside range expansion from prior close)",
    "short": "Low falls to prev_close - 0.8*ATR (downside range expansion from prior close)",
    "desc": "Volatility breakout: 0.8 ATR intrabar expansion from prior close signals trend continuation",
    "source": "trade_your_way_to_financial_freedom -- Ch.8 Volatility Breakouts (Wilder New Concepts in Technical Trading)",
}

_K = 0.8


def signal(ind, pos, htf=None):
    """Intrabar high/low crosses prev_close +/- 0.8*ATR -> breakout entry."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    c1 = ind["close"][pos - 1]
    a = ind["atr"][pos]
    if nan(h, l, c1, a):
        return None
    threshold = _K * a
    if h >= c1 + threshold:
        return "long"
    if l <= c1 - threshold:
        return "short"
    return None
