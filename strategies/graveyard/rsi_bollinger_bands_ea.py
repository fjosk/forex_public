#!/usr/bin/env python3
"""rsi_bollinger_bands_ea -- RSI vs fixed 30/70 thresholds + srsi_k dynamic band proxy. MQL5 raposter 2016."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_bollinger_bands_ea",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "rsi, srsi_k",
    "long": "RSI < 30 (Trigger 1) OR srsi_k < 20 (dynamic oversold proxy, Trigger 2)",
    "short": "RSI > 70 (Trigger 1) OR srsi_k > 80 (dynamic overbought proxy, Trigger 2)",
    "desc": "RSI Bollinger Bands Combined EA: fixed RSI levels with Stochastic RSI dynamic band proxy",
    "source": "MQL5 CodeBase raposter 2016 (mql5.com/en/code/14628)",
}


def signal(ind, pos, htf=None):
    """RSI fixed threshold OR Stochastic RSI extreme as dual-trigger mean reversion."""
    r = ind["rsi"][pos]
    sk = ind["srsi_k"][pos]
    if nan(r, sk):
        return None
    # Trigger 1: classic RSI thresholds
    # Trigger 2: srsi_k as proxy for RSI-below-its-own-lower-BB
    if r < 30 or sk < 20:
        return "long"
    if r > 70 or sk > 80:
        return "short"
    return None
