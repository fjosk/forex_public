#!/usr/bin/env python3
"""volatility_breakout_entry_atr_from_open -- Volatility Breakout Entry (ATR Move From Open): enter when price moves 1.5 x ATR from today's open; uses intrabar high/low vs open threshold. Tharp Appendix II.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "volatility_breakout_entry_atr_from_open",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "atr, open, high, low",
    "long": "High >= open + 1.5*ATR (upside ATR expansion from today's open)",
    "short": "Low <= open - 1.5*ATR (downside ATR expansion from today's open)",
    "desc": "Volatility breakout from open: 1.5 ATR intrabar expansion off the day's open price signals trend entry",
    "source": "trade_your_way_to_financial_freedom -- Appendix II Key Terms Volatility Breakout definition",
}

_K = 1.5


def signal(ind, pos, htf=None):
    """Intrabar high/low crosses open +/- 1.5*ATR -> breakout in that direction."""
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    a = ind["atr"][pos]
    if nan(o, h, l, a):
        return None
    threshold = _K * a
    if h >= o + threshold:
        return "long"
    if l <= o - threshold:
        return "short"
    return None
