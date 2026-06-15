#!/usr/bin/env python3
"""connors_rsi2_mean_reversion -- Connors RSI-2 mean reversion with SMA100 trend filter. web:fmzquant."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "connors_rsi2_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1d",
    "indicators": "rsi2, sma100, close",
    "long": "close above SMA100 (trend up) and RSI(2) < 10",
    "short": "close below SMA100 (trend down) and RSI(2) > 90",
    "desc": "Larry Connors RSI-2 mean reversion: trend filter via SMA100, enter on RSI(2) extreme",
    "source": "web:https://medium.com/@FMZQuant/larry-connors-rsi2-mean-reversion-strategy-861f5a3579e3",
}


def signal(ind, pos, htf=None):
    """Connors RSI-2 mean reversion."""
    c = ind["close"][pos]
    r2 = ind["rsi2"][pos]
    s100 = ind["sma100"][pos]
    if nan(c, r2, s100):
        return None
    if c > s100 and r2 < 10:
        return "long"
    if c < s100 and r2 > 90:
        return "short"
    return None
