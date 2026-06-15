#!/usr/bin/env python3
"""rsi_cci_dual_oscillator -- RSI + CCI dual extreme confirmation entry. TheForexGeek."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_cci_dual_oscillator",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h/4h",
    "indicators": "rsi, cci",
    "long": "RSI < 30 AND CCI < -100 (dual oversold confirmation)",
    "short": "RSI > 70 AND CCI > 100 (dual overbought confirmation)",
    "desc": "RSI + CCI dual oscillator extreme: both must confirm oversold/overbought",
    "source": "web:https://theforexgeek.com/rsi-cci-strategy/",
}


def signal(ind, pos, htf=None):
    """Both RSI and CCI must agree on extreme: dual-confirmation mean reversion."""
    r = ind["rsi"][pos]
    cci = ind["cci"][pos]
    if nan(r, cci):
        return None

    if r < 30 and cci < -100:
        return "long"
    if r > 70 and cci > 100:
        return "short"

    return None
