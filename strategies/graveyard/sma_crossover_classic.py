#!/usr/bin/env python3
"""sma_crossover_classic -- SMA10/20 crossover (10/30 original, 20 proxy). mementum backtrader."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "sma_crossover_classic",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "sma10, sma20",
    "long": "SMA10 crosses above SMA20 (golden cross; SMA20 proxies original SMA30)",
    "short": "SMA10 crosses below SMA20 (death cross)",
    "desc": "Classic SMA10/20 dual-MA crossover (source uses 10/30; SMA20 is closest proxy)",
    "source": "mementum/backtrader official library SmaCross strategy (Python)",
}


def signal(ind, pos, htf=None):
    """Enter on SMA10 vs SMA20 crossover."""
    f = ind["sma10"][pos]
    s = ind["sma20"][pos]
    f1 = ind["sma10"][pos - 1]
    s1 = ind["sma20"][pos - 1]
    if nan(f, s, f1, s1):
        return None
    if _xup(f, f1, s, s1):
        return "long"
    if _xdn(f, f1, s, s1):
        return "short"
    return None
