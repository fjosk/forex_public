#!/usr/bin/env python3
"""kst_signal_crossover -- KST line crosses its 9-period signal line. Nikhil Adithyan / Martin Pring."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "kst_signal_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1d",
    "indicators": "kst, kst_sig",
    "long": "KST crosses above its signal line (9-period SMA of KST) from below",
    "short": "KST crosses below its signal line from above",
    "desc": "KST (Know Sure Thing) signal line crossover; four-cycle weighted ROC momentum",
    "source": "Nikhil Adithyan KST Python backtest (medium.com/codex); Martin Pring KST oscillator",
}


def signal(ind, pos, htf=None):
    """KST crosses above/below its signal line."""
    k = ind["kst"][pos]
    k1 = ind["kst"][pos - 1]
    ks = ind["kst_sig"][pos]
    ks1 = ind["kst_sig"][pos - 1]
    if nan(k, k1, ks, ks1):
        return None
    if _xup(k, k1, ks, ks1):
        return "long"
    if _xdn(k, k1, ks, ks1):
        return "short"
    return None
