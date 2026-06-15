#!/usr/bin/env python3
"""two_amigos_adx_price -- ADX > 20 with 20-bar price momentum. Kevin Davey entry #28."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "two_amigos_adx_price",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "adx, close",
    "long": "ADX > 20 AND close > close[pos-20]",
    "short": "ADX > 20 AND close < close[pos-20]",
    "desc": "Two Amigos: ADX trend gate with 20-bar price momentum direction",
    "source": "Kevin Davey 'Entry and Exit Confessions of a Champion Trader' entry #28; zeta-zetra.github.io",
}


def signal(ind, pos, htf=None):
    """ADX confirms trend; direction from price vs 20 bars ago."""
    adx_val = ind["adx"][pos]
    c = ind["close"][pos]
    c20 = ind["close"][pos - 20]
    if nan(adx_val, c, c20):
        return None
    if adx_val <= 20:
        return None
    if c > c20:
        return "long"
    if c < c20:
        return "short"
    return None
