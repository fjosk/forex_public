#!/usr/bin/env python3
"""rsi_oversold_trend_filter -- RSI mean reversion gated by ADX range filter. armelf/Financial-Algorithms GitHub."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_oversold_trend_filter",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "rsi, adx",
    "long": "ADX < 20 (ranging market) AND RSI < 30 (oversold)",
    "short": "ADX < 20 (ranging market) AND RSI > 70 (overbought)",
    "desc": "RSI oversold/overbought entries only in ranging markets (ADX < 20 gate)",
    "source": "armelf/Financial-Algorithms GitHub",
}

_ADX_RANGE_THRESHOLD = 20.0


def signal(ind, pos, htf=None):
    """RSI mean reversion entered only when market is ranging (low ADX)."""
    r = ind["rsi"][pos]
    a = ind["adx"][pos]
    if nan(r, a):
        return None
    ranging = a < _ADX_RANGE_THRESHOLD
    if not ranging:
        return None
    if r < 30:
        return "long"
    if r > 70:
        return "short"
    return None
