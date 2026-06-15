#!/usr/bin/env python3
"""bb_rsi_percent_b -- Bollinger %B cross + RSI zone mean-reversion entries. armelf Financial-Algorithms."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "bb_rsi_percent_b",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "bb_pctb, rsi",
    "long": "bb_pctb crosses above 0 OR (bb_pctb < 0.2 AND rsi <= 50)",
    "short": "bb_pctb > 0.8 AND rsi >= 50",
    "desc": "Bollinger %B cross of lower band + RSI zone filter for mean-reversion entries",
    "source": "web:https://github.com/armelf/Financial-Algorithms",
}


def signal(ind, pos, htf=None):
    """BB %B cross above 0 or extreme low zone with RSI filter."""
    pctb = ind["bb_pctb"][pos]
    pctb1 = ind["bb_pctb"][pos - 1]
    rsi = ind["rsi"][pos]
    if nan(pctb, pctb1, rsi):
        return None
    # Long: %B crosses above 0 (price exits below lower band)
    if _xup(pctb, pctb1, 0, 0):
        return "long"
    # Long: extreme low zone with RSI not extended
    if pctb < 0.2 and rsi <= 50:
        return "long"
    # Short: near upper band with neutral/high RSI
    if pctb > 0.8 and rsi >= 50:
        return "short"
    return None
