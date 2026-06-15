#!/usr/bin/env python3
"""CHOP -- Choppiness-regime-exit breakout. sister-lab live roster (tier3, forward-test add).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "CHOP",
    "cadences": ['swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "Choppiness Index(14), EMA50",
    "long": "CHOP drops through 38.2 & close>EMA50",
    "short": "CHOP drops through 38.2 & close<EMA50",
    "desc": "Choppiness-regime-exit breakout",
    "source": "sister-lab live roster (tier3, forward-test add)",
}


def signal(ind, pos, htf=None):
    """Choppiness-regime-exit breakout."""
    ch, ch1, c, e = ind["chop"][pos], ind["chop"][pos - 1], ind["close"][pos], ind["ema50"][pos]
    if nan(ch, ch1, c, e):
        return None
    if ch1 >= 38.2 and ch < 38.2:
        if c > e:
            return "long"
        if c < e:
            return "short"
    return None
