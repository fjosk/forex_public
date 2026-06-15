#!/usr/bin/env python3
"""ICHI -- Ichimoku TK cross in cloud direction. sister-lab live roster (tier3, full-gauntlet survivor on crypto).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ICHI",
    "cadences": ['swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "Ichimoku (tenkan/kijun/senkou A,B)",
    "long": "tenkan crosses above kijun & close above cloud",
    "short": "tenkan crosses below kijun & close below cloud",
    "desc": "Ichimoku TK cross in cloud direction",
    "source": "sister-lab live roster (tier3, full-gauntlet survivor on crypto)",
}


def signal(ind, pos, htf=None):
    """Ichimoku TK cross in cloud direction."""
    ten, kij = ind["ich_ten"][pos], ind["ich_kij"][pos]
    ten1, kij1 = ind["ich_ten"][pos - 1], ind["ich_kij"][pos - 1]
    c, a, b = ind["close"][pos], ind["ich_a"][pos], ind["ich_b"][pos]
    if nan(ten, kij, ten1, kij1, c, a, b):
        return None
    top, bot = max(a, b), min(a, b)
    if ten > kij and ten1 <= kij1 and c > top:
        return "long"
    if ten < kij and ten1 >= kij1 and c < bot:
        return "short"
    return None
