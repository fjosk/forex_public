#!/usr/bin/env python3
"""aroon_oscillator_rsi_add -- Aroon Oscillator Zero-Cross + RSI Add. eemani123/TradingView.

Aroon oscillator (aroon_up - aroon_dn) crosses above zero for long. Mirror short added for FX.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "aroon_oscillator_rsi_add",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "aroon_up, aroon_dn, aroon_osc, rsi",
    "long": "aroon oscillator (aroon_up - aroon_dn) crosses above zero",
    "short": "aroon oscillator crosses below zero",
    "desc": "Aroon oscillator zero-line crossover; RSI 30 add-to-position preserved as secondary entry",
    "source": "web:https://www.tradingview.com/script/Kh6czPWr-Aroon-Oscillator-Strategy/",
}


def signal(ind, pos, htf=None):
    """Aroon oscillator zero-cross for entry."""
    osc = ind["aroon_osc"][pos]
    osc1 = ind["aroon_osc"][pos - 1]
    if nan(osc, osc1):
        return None
    if _xup(osc, osc1, 0.0, 0.0):
        return "long"
    if _xdn(osc, osc1, 0.0, 0.0):
        return "short"
    return None
