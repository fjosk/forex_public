#!/usr/bin/env python3
"""rsi2_oversold_mean_reversion -- RSI(2) extreme levels; exit on prior-bar high/low breach. QuantConnect 2022."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi2_oversold_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "rsi2, close, high, low",
    "long": "rsi2 < 15 (extreme short-term oversold)",
    "short": "rsi2 > 85 (extreme short-term overbought, FX mirror)",
    "desc": "RSI(2) extreme oversold/overbought mean reversion; exit on prior-bar high/low recovery",
    "source": "QuantConnect forum (quantconnect.com/forum/discussion/15754); community RSI-2 strategy 2022",
}


def signal(ind, pos, htf=None):
    """Enter on RSI(2) extreme; REVERT archetype handles the ATR exit."""
    r2 = ind["rsi2"][pos]
    if nan(r2):
        return None
    if r2 < 15:
        return "long"
    if r2 > 85:
        return "short"
    return None
