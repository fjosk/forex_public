#!/usr/bin/env python3
"""jesse_sma_crossover -- Golden/death cross SMA50 vs SMA200. jesse-ai official example."""
from strategies._common import nan, TREND_FLIP, _xup, _xdn, ALL_CLASSES

META = {
    "id": "jesse_sma_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "sma50, sma200",
    "long": "sma50 crosses above sma200 (golden cross)",
    "short": "sma50 crosses below sma200 (death cross)",
    "desc": "Golden/death cross: SMA50 vs SMA200 dual crossover system",
    "source": "https://github.com/jesse-ai/example-strategies/blob/master/SMACrossover/__init__.py",
}


def signal(ind, pos, htf=None):
    """SMA50 vs SMA200 crossover."""
    s50 = ind["sma50"][pos]
    s50_1 = ind["sma50"][pos - 1]
    s200 = ind["sma200"][pos]
    s200_1 = ind["sma200"][pos - 1]
    if nan(s50, s50_1, s200, s200_1):
        return None
    if _xup(s50, s50_1, s200, s200_1):
        return "long"
    if _xdn(s50, s50_1, s200, s200_1):
        return "short"
    return None
