#!/usr/bin/env python3
"""ATRC -- ATR-channel breakout. sister-lab live roster (tier3).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ATRC",
    "cadences": ['swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "EMA20, ATR14",
    "long": "close > EMA20 + 2*ATR & EMA20 rising",
    "short": "close < EMA20 - 2*ATR & EMA20 falling",
    "desc": "ATR-channel breakout",
    "source": "sister-lab live roster (tier3)",
}


def signal(ind, pos, htf=None):
    """ATR-channel breakout."""
    c, e20, atr, e20p5 = ind["close"][pos], ind["ema20"][pos], ind["atr"][pos], ind["ema20"][pos - 5]
    if nan(c, e20, atr, e20p5) or atr <= 0:
        return None
    if c > e20 + 2.0 * atr and e20 > e20p5:
        return "long"
    if c < e20 - 2.0 * atr and e20 < e20p5:
        return "short"
    return None
