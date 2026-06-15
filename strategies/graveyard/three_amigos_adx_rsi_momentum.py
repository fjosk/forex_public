#!/usr/bin/env python3
"""three_amigos_adx_rsi_momentum -- ADX + RSI + dual lookback momentum. Kevin Davey entry #27."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "three_amigos_adx_rsi_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "adx, rsi, close",
    "long": "ADX > 25 AND rsi < 50 AND close < close[pos-20] AND close > close[pos-10]",
    "short": "ADX > 25 AND rsi > 50 AND close > close[pos-20] AND close < close[pos-10]",
    "desc": "Three Amigos: ADX trend strength + RSI midline + dual 10/20-bar price lookback",
    "source": "Kevin Davey 'Entry and Exit Confessions of a Champion Trader' entry #27; zeta-zetra.github.io",
}


def signal(ind, pos, htf=None):
    """ADX gates; RSI and 10/20-bar close lookbacks give direction."""
    adx_val = ind["adx"][pos]
    rsi_val = ind["rsi"][pos]
    c = ind["close"][pos]
    c10 = ind["close"][pos - 10]
    c20 = ind["close"][pos - 20]
    if nan(adx_val, rsi_val, c, c10, c20):
        return None
    if adx_val <= 25:
        return None
    if rsi_val < 50 and c < c20 and c > c10:
        return "long"
    if rsi_val > 50 and c > c20 and c < c10:
        return "short"
    return None
