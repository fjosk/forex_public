#!/usr/bin/env python3
"""hackingmarkets_supertrend -- Supertrend ATR trend-following on direction flip. hackingthemarkets / Python ccxt.

st_dir is the precomputed Supertrend direction flag (+1 uptrend, -1 downtrend). Enter long on the
bar st_dir flips to +1; enter short when it flips to -1. Exit on the opposing flip (TREND_FLIP).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "hackingmarkets_supertrend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "st_dir, atr",
    "long": "st_dir flips from -1 to +1 (Supertrend turns bullish)",
    "short": "st_dir flips from +1 to -1 (Supertrend turns bearish)",
    "desc": "Supertrend ATR trend-following: enter on direction flip, exit on reversal",
    "source": "https://github.com/hackingthemarkets/supertrend-crypto-bot/blob/main/supertrend.py",
}


def signal(ind, pos, htf=None):
    """Supertrend direction flip entry."""
    d = ind["st_dir"][pos]
    d1 = ind["st_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d == 1 and d1 == -1:
        return "long"
    if d == -1 and d1 == 1:
        return "short"
    return None
