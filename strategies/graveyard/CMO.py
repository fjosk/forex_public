#!/usr/bin/env python3
"""CMO -- Chande Momentum zero-cross with EMA200 trend filter. sister-lab live roster (tier3, forward-test add).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "CMO",
    "cadences": ['swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "CMO(20), EMA200",
    "long": "CMO crosses up through 0 & close>EMA200",
    "short": "CMO crosses down through 0 & close<EMA200",
    "desc": "Chande Momentum zero-cross with EMA200 trend filter",
    "source": "sister-lab live roster (tier3, forward-test add)",
}


def signal(ind, pos, htf=None):
    """Chande Momentum zero-cross with EMA200 trend filter."""
    c, c1, e200, px = ind["cmo"][pos], ind["cmo"][pos - 1], ind["ema200"][pos], ind["close"][pos]
    if nan(c, c1, e200, px):
        return None
    if c > 0 and c1 <= 0 and px > e200:
        return "long"
    if c < 0 and c1 >= 0 and px < e200:
        return "short"
    return None
