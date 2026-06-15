#!/usr/bin/env python3
"""macd_histogram_slope_tick_common_signal -- MACD-Histogram slope reversal: tick up from down-sequence -> long; tick down from up-sequence -> short. Elder.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_histogram_slope_tick_common_signal",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd_hist",
    "long": "MACD-Histogram flips from falling to rising (slope turns positive)",
    "short": "MACD-Histogram flips from rising to falling (slope turns negative)",
    "desc": "Elder MACD-H slope reversal: histogram tick-up after decline = long; tick-down after rise = short",
    "source": "Elder, Trading for a Living, Sec 26 MACD-Histogram Trading Rules, Fig 26-3, p.132-133",
}


def signal(ind, pos, htf=None):
    """MACD-Histogram slope flip: down-to-up = long; up-to-down = short."""
    if pos < 2:
        return None
    h = ind["macd_hist"][pos]
    h1 = ind["macd_hist"][pos - 1]
    h2 = ind["macd_hist"][pos - 2]
    if nan(h, h1, h2):
        return None
    # Slope flips from down to up
    if h > h1 and h1 < h2:
        return "long"
    # Slope flips from up to down
    if h < h1 and h1 > h2:
        return "short"
    return None
