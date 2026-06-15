#!/usr/bin/env python3
"""RSI14 -- RSI(14) reversal with EMA200 trend filter. sister-lab live roster (tier3).

Price/OHLC only (no volume) -> FX-applicable. Signal logic ported from the sister-lab roster; it must
still clear the FOREX gauntlet on Ostium costs to earn a forward/live wiring. Self-contained module:
META (definition the loader reads) + signal() (the decision function the engine + future Ostium
trader both call). See strategies/README.md for the standard + lifecycle.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "RSI14",
    "cadences": ['swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "RSI14, EMA200",
    "long": "close>EMA200 & RSI crosses up through 30",
    "short": "close<EMA200 & RSI crosses down through 70",
    "desc": "RSI(14) reversal with EMA200 trend filter",
    "source": "sister-lab live roster (tier3)",
}


def signal(ind, pos, htf=None):
    """RSI(14) reversal with EMA200 trend filter."""
    r, r1, c, e200 = ind["rsi"][pos], ind["rsi"][pos - 1], ind["close"][pos], ind["ema200"][pos]
    if nan(r, r1, c, e200):
        return None
    if c > e200 and r > 30 and r1 <= 30:
        return "long"
    if c < e200 and r < 70 and r1 >= 70:
        return "short"
    return None
