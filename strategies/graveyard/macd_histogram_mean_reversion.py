#!/usr/bin/env python3
"""macd_histogram_mean_reversion -- 4-bar MACD histogram decline mean reversion. QuantifiedStrategies."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "macd_histogram_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "daily",
    "indicators": "macd_hist, close",
    "long": "MACD histogram declining 4 bars, 4th bar below zero, current close below prior close",
    "short": "MACD histogram rising 4 bars, 4th bar above zero, current close above prior close",
    "desc": "MACD histogram 4-bar decline mean reversion entry",
    "source": "web:https://www.quantifiedstrategies.com/macd-histogram/",
}


def signal(ind, pos, htf=None):
    """4 consecutive declining histogram bars, 4th below zero, close below prev -> long."""
    if pos < 4:
        return None
    h0 = ind["macd_hist"][pos]
    h1 = ind["macd_hist"][pos - 1]
    h2 = ind["macd_hist"][pos - 2]
    h3 = ind["macd_hist"][pos - 3]
    c0 = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    if nan(h0, h1, h2, h3, c0, c1):
        return None

    # Long: 4 consecutive declining bars, last below zero, close falling
    if h0 < h1 < h2 < h3 and h0 < 0 and c0 < c1:
        return "long"

    # Short: 4 consecutive rising bars, last above zero, close rising
    if h0 > h1 > h2 > h3 and h0 > 0 and c0 > c1:
        return "short"

    return None
