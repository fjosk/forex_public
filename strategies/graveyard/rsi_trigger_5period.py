#!/usr/bin/env python3
"""rsi_trigger_5period -- RSI(14) below OB threshold + close vs SMA5. Kevin Davey RSI Trigger.

Source uses RSI(5); rsi (14-period) is the closest available key.
Thresholds adjusted: RSI(14) < 70 approximates RSI(5) < 80 logic (fewer extremes at longer period).
close_sma5 is available directly.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_trigger_5period",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "rsi, close_sma5, close",
    "long": "rsi < 70 AND close > close_sma5 (momentum not yet overbought, price above fast avg)",
    "short": "rsi > 30 AND close < close_sma5 (momentum not yet oversold, price below fast avg)",
    "desc": "RSI trigger: momentum not at extreme + price above/below 5-bar SMA; Kevin Davey concept",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/books/rsi_trigger.html",
}


def signal(ind, pos, htf=None):
    """RSI below OB zone AND close above 5-bar SMA for long; mirror for short."""
    r = ind["rsi"][pos]
    sma5 = ind["close_sma5"][pos]
    c = ind["close"][pos]
    if nan(r, sma5, c):
        return None
    if r < 70 and c > sma5:
        return "long"
    if r > 30 and c < sma5:
        return "short"
    return None
