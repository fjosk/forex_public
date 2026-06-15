#!/usr/bin/env python3
"""adx_rsi_direction -- ADX Trend Strength + RSI Direction. Nikhil-Adithyan/Algorithmic-Trading-with-Python.

ADX > 35 confirms strong trend. DI crossover sets direction, RSI 50 acts as final gate.
Note: per source, DI- > DI+ with RSI < 50 triggers LONG (countertrend / contrarian logic --
preserved as-sourced).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_rsi_direction",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "adx, di_plus, di_minus, rsi",
    "long": "adx > 35 AND di_minus > di_plus AND rsi < 50 (as-sourced: DI- dominance + RSI not extreme)",
    "short": "adx > 35 AND di_plus > di_minus AND rsi > 50",
    "desc": "ADX trend-strength gate with DI direction and RSI 50 filter (as-sourced contrarian DI logic)",
    "source": "web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """ADX strength + DI direction + RSI 50 gate."""
    dx = ind["adx"][pos]
    dp = ind["di_plus"][pos]
    dm = ind["di_minus"][pos]
    r = ind["rsi"][pos]
    if nan(dx, dp, dm, r):
        return None
    if dx > 35 and dp < dm and r < 50:
        return "long"
    if dx > 35 and dp > dm and r > 50:
        return "short"
    return None
