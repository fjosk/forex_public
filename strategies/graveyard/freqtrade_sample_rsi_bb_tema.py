#!/usr/bin/env python3
"""freqtrade_sample_rsi_bb_tema -- RSI cross + TEMA vs BB midline + TEMA slope. freqtrade official template."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "freqtrade_sample_rsi_bb_tema",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "rsi, bb_mid, tema9",
    "long": "RSI crosses above 30 AND TEMA9 <= BB_mid AND TEMA9 rising",
    "short": "RSI crosses above 70 AND TEMA9 > BB_mid AND TEMA9 falling",
    "desc": "Freqtrade sample strategy: RSI oversold cross + TEMA position vs BB midline + TEMA direction",
    "source": "freqtrade/freqtrade official sample_strategy.py (develop branch)",
}


def signal(ind, pos, htf=None):
    """RSI crossover with TEMA/BB confirmation and TEMA slope direction filter."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    tema = ind["tema9"][pos]
    tema1 = ind["tema9"][pos - 1]
    bbm = ind["bb_mid"][pos]
    if nan(r, r1, tema, tema1, bbm):
        return None
    tema_rising = tema > tema1
    tema_falling = tema < tema1
    # Long: RSI crosses above 30, TEMA below or at BB mid, TEMA rising
    if r > 30 and r1 <= 30 and tema <= bbm and tema_rising:
        return "long"
    # Short: RSI crosses above 70, TEMA above BB mid, TEMA falling
    if r > 70 and r1 <= 70 and tema > bbm and tema_falling:
        return "short"
    return None
