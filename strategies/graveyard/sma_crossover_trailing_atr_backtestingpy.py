#!/usr/bin/env python3
"""sma_crossover_trailing_atr_backtestingpy -- SMA10/20 crossover with ATR trailing stop. backtesting.py."""
from strategies._common import nan, TREND, ALL_CLASSES, _xup, _xdn

META = {
    "id": "sma_crossover_trailing_atr_backtestingpy",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "sma10, sma20, atr",
    "long": "SMA10 crosses above SMA20 (SMA20 proxies SMA25)",
    "short": "Not implemented in source; symmetric short added",
    "desc": "SMA10/20 crossover entry with ATR-based trailing stop exit (backtesting.py SmaCross)",
    "source": "backtesting.py Strategies Library -- SmaCross + TrailingStrategy (kernc.github.io)",
}


def signal(ind, pos, htf=None):
    """SMA10/20 crossover; ATR trail managed by exit envelope."""
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
