#!/usr/bin/env python3
"""bb_keltner_squeeze_rsi -- BB wider than KC (squeeze release) + RSI extreme. Nikhil-Adithyan."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bb_keltner_squeeze_rsi",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "bb_lo, bb_up, kc_lo, kc_up, rsi",
    "long": "bb_lo < kc_lo AND bb_up > kc_up (squeeze released) AND rsi < 30",
    "short": "squeeze released AND rsi > 70",
    "desc": "BB/KC squeeze release with RSI extreme confirmation; Nikhil-Adithyan Python",
    "source": "web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """Volatility expansion (BB wider than KC) plus RSI extreme entry."""
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    kc_up = ind["kc_up"][pos]
    rsi = ind["rsi"][pos]
    if nan(bb_lo, bb_up, kc_lo, kc_up, rsi):
        return None
    squeeze_released = bb_lo < kc_lo and bb_up > kc_up
    if not squeeze_released:
        return None
    if rsi < 30:
        return "long"
    if rsi > 70:
        return "short"
    return None
