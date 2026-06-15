#!/usr/bin/env python3
"""volatility_breakout_entry_0_7x_atr -- Volatility Breakout Entry (0.7x ATR Move): enter long/short when the intrabar move from the prior close equals or exceeds 0.7 x ATR(5). Tharp Ch.11.

Price/OHLC only. No volume.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "volatility_breakout_entry_0_7x_atr",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "atr, high, low, close",
    "long": "High >= prev_close + 0.7*ATR(5) (high-probability low-R upside breakout)",
    "short": "Low <= prev_close - 0.7*ATR(5) (high-probability low-R downside breakout)",
    "desc": "0.7 ATR intrabar breakout entry: high-probability short-R move off prior close; tight ATR stop/target",
    "source": "trade_your_way_to_financial_freedom -- Ch.11 High-Probability Low R-Multiple Trading example",
}

# Spec uses ATR(5) but engine provides ATR(14); closest available is atr
_K = 0.7


def signal(ind, pos, htf=None):
    """Intrabar move of 0.7*ATR from prior close -> entry."""
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
