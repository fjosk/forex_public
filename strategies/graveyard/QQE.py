#!/usr/bin/env python3
"""QQE -- QQE smoothed-RSI trailing-line cross. sister-lab live roster (tier3).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, QQE_EXIT, ALL_CLASSES

META = {
    "id": "QQE",
    "cadences": ['swing'],
    "exit": QQE_EXIT,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "QQE (smoothed RSI + trailing line)",
    "long": "rsi_ma crosses above qqe line while >50",
    "short": "rsi_ma crosses below qqe line while <50",
    "desc": "QQE smoothed-RSI trailing-line cross",
    "source": "sister-lab live roster (tier3)",
}


def signal(ind, pos, htf=None):
    """QQE smoothed-RSI trailing-line cross."""
    r, l = ind["qqe_rsima"][pos], ind["qqe_line"][pos]
    r1, l1 = ind["qqe_rsima"][pos - 1], ind["qqe_line"][pos - 1]
    if nan(r, l, r1, l1):
        return None
    if r > l and r1 <= l1 and r > 50:
        return "long"
    if r < l and r1 >= l1 and r < 50:
        return "short"
    return None
