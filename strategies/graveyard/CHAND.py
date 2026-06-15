#!/usr/bin/env python3
"""CHAND -- Chandelier-exit direction flip. sister-lab live roster (tier3, forward-test add).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "CHAND",
    "cadences": ['swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "Chandelier Exit direction",
    "long": "chandelier direction flips -1 -> +1",
    "short": "chandelier direction flips +1 -> -1",
    "desc": "Chandelier-exit direction flip",
    "source": "sister-lab live roster (tier3, forward-test add)",
}


def signal(ind, pos, htf=None):
    """Chandelier-exit direction flip."""
    d, d1 = ind["chand_dir"][pos], ind["chand_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d == 1 and d1 == -1:
        return "long"
    if d == -1 and d1 == 1:
        return "short"
    return None
