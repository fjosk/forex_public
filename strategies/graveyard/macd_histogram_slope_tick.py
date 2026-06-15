#!/usr/bin/env python3
"""macd_histogram_slope_tick -- MACD-Histogram minor tick: one-bar slope up = long signal; one-bar slope down = short signal. Elder (Come Into My Trading Room).

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_histogram_slope_tick",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd_hist",
    "long": "MACD-Histogram bar > previous bar (bulls strengthening)",
    "short": "MACD-Histogram bar < previous bar (bears strengthening)",
    "desc": "Elder minor MACD-H signal: single bar slope as a momentum direction cue",
    "source": "Elder, Come Into My Trading Room, Ch5 MACD-Histogram The Strongest Signal, p.104-105",
}


def signal(ind, pos, htf=None):
    """MACD-Histogram one-bar slope direction."""
    if pos < 1:
        return None
    h = ind["macd_hist"][pos]
    h1 = ind["macd_hist"][pos - 1]
    if nan(h, h1):
        return None
    if h > h1:
        return "long"
    if h < h1:
        return "short"
    return None
