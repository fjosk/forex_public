#!/usr/bin/env python3
"""kst_signal_cross -- KST crosses above/below its signal line. Martin Pring / EarnForex."""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "kst_signal_cross",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "daily/weekly",
    "indicators": "kst, kst_sig",
    "long": "KST line crosses above its signal line from below",
    "short": "KST line crosses below its signal line from above",
    "desc": "KST signal-line crossover: Know Sure Thing oscillator momentum entry",
    "source": "web:https://www.earnforex.com/guides/trading-strategies/",
}


def signal(ind, pos, htf=None):
    """KST vs signal-line cross: long on bullish cross, short on bearish."""
    if pos < 1:
        return None
    k0 = ind["kst"][pos]
    ks0 = ind["kst_sig"][pos]
    k1 = ind["kst"][pos - 1]
    ks1 = ind["kst_sig"][pos - 1]
    if nan(k0, ks0, k1, ks1):
        return None

    if _xup(k0, k1, ks0, ks1):
        return "long"
    if _xdn(k0, k1, ks0, ks1):
        return "short"

    return None
