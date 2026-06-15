#!/usr/bin/env python3
"""supertrend_adx_sma_futures -- ADX-gated SMA10/50 crossover bidirectional. freqtrade FAdxSmaStrategy."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "supertrend_adx_sma_futures",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "adx, sma10, sma50",
    "long": "ADX > 30 AND sma10 crosses above sma50 (SMA12/48 proxied by SMA10/50)",
    "short": "ADX > 30 AND sma10 crosses below sma50",
    "desc": "ADX > 30 gated SMA crossover bidirectional futures strategy (FAdxSmaStrategy)",
    "source": "freqtrade/freqtrade-strategies futures/FAdxSmaStrategy.py; SMA10/50 proxy for 12/48",
}


def signal(ind, pos, htf=None):
    """ADX > 30 gates the trade; direction from SMA10/50 crossover."""
    adx_val = ind["adx"][pos]
    f = ind["sma10"][pos]
    s = ind["sma50"][pos]
    f1 = ind["sma10"][pos - 1]
    s1 = ind["sma50"][pos - 1]
    if nan(adx_val, f, s, f1, s1):
        return None
    if adx_val <= 30:
        return None
    if _xup(f, f1, s, s1):
        return "long"
    if _xdn(f, f1, s, s1):
        return "short"
    return None
