#!/usr/bin/env python3
"""B1 -- MACD weak-rally SELL, short-only. sister-lab live roster (tier3).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, B1_EXIT, ALL_CLASSES

META = {
    "id": "B1",
    "cadences": ['day'],
    "exit": B1_EXIT,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h",
    "indicators": "MACD(12,26,9)",
    "long": "(none -- short only)",
    "short": "close>close[-3] & macd<=0 & hist<0 & hist falling",
    "desc": "MACD weak-rally SELL, short-only",
    "source": "sister-lab live roster (tier3)",
}


def signal(ind, pos, htf=None):
    """MACD weak-rally SELL, short-only."""
    c, c3 = ind["close"][pos], ind["close"][pos - 3]
    ml, mh, mh1 = ind["macd"][pos], ind["macd_hist"][pos], ind["macd_hist"][pos - 1]
    if nan(c, c3, ml, mh, mh1):
        return None
    if c > c3 and ml <= 0 and mh < 0 and mh < mh1:
        return "short"
    return None
