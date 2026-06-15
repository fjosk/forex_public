#!/usr/bin/env python3
"""rsi_overbought_oversold_daily_forex -- RSI 25/75 deep mean reversion; exit at RSI 50. QuantConnect/lites.e 2024."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_overbought_oversold_daily_forex",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "rsi, close",
    "long": "RSI < 25 (extreme oversold on daily)",
    "short": "RSI > 75 (extreme overbought on daily)",
    "desc": "RSI 14 daily FX mean reversion with 25/75 deep levels; exit at RSI 50 neutrality",
    "source": "QuantConnect RSI FX implementation (medium.com/@lites.e, 2024)",
}


def signal(ind, pos, htf=None):
    """Enter at RSI extremes; exit handled by REVERT archetype ATR envelope."""
    r = ind["rsi"][pos]
    if nan(r):
        return None
    if r < 25:
        return "long"
    if r > 75:
        return "short"
    return None
