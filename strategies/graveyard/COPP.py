#!/usr/bin/env python3
"""COPP -- Coppock curve zero-cross flip. sister-lab live roster (tier3).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "COPP",
    "cadences": ['swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "Coppock curve",
    "long": "Coppock crosses up through 0",
    "short": "Coppock crosses down through 0",
    "desc": "Coppock curve zero-cross flip",
    "source": "sister-lab live roster (tier3)",
}


def signal(ind, pos, htf=None):
    """Coppock curve zero-cross flip."""
    cp, cp1 = ind["coppock"][pos], ind["coppock"][pos - 1]
    if nan(cp, cp1):
        return None
    if cp > 0 and cp1 <= 0:
        return "long"
    if cp < 0 and cp1 >= 0:
        return "short"
    return None
