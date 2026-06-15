#!/usr/bin/env python3
"""bollinger_rsi_macd -- Bollinger Band Mean-Reversion + RSI + MACD. Pine BB-RSI-MACD."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bollinger_rsi_macd",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_lo, bb_up, bb_mid, rsi, macd_hist",
    "long": "three-bar recovery from below bb_lo; close still below bb_mid; rsi < 50; macd_hist > 0",
    "short": "three-bar decline from above bb_up; close still above bb_mid; rsi > 50; macd_hist < 0",
    "desc": "Three-bar BB reversal sequence confirmed by RSI below midpoint and bullish MACD histogram",
    "source": "github.com/hasnocool/tradingview-pine-scripts BB RSI MACD v1.0.pine",
}


def signal(ind, pos, htf=None):
    """Three-bar BB setup confirmed by RSI and MACD histogram."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    c2 = ind["close"][pos - 2]
    bbl = ind["bb_lo"][pos]
    bbu = ind["bb_up"][pos]
    bbm = ind["bb_mid"][pos]
    r = ind["rsi"][pos]
    mh = ind["macd_hist"][pos]
    if nan(c, c1, c2, bbl, bbu, bbm, r, mh):
        return None
    setup_long = c2 < bbl and c1 > c2 and c > c1 and c < bbm and r < 50 and mh > 0
    setup_short = c2 > bbu and c1 < c2 and c < c1 and c > bbm and r > 50 and mh < 0
    if setup_long:
        return "long"
    if setup_short:
        return "short"
    return None
