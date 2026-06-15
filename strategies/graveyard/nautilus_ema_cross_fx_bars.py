#!/usr/bin/env python3
"""nautilus_ema_cross_fx_bars -- EMA fast/slow crossover, NautilusTrader FX tutorial. nautilustrader.io.

Fast EMA(5) crosses slow EMA(20): classic golden/death cross on FX bars.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "nautilus_ema_cross_fx_bars",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5, ema20",
    "long": "EMA5 crosses above EMA20 (golden cross)",
    "short": "EMA5 crosses below EMA20 (death cross)",
    "desc": "EMA fast/slow crossover (NautilusTrader FX bars tutorial)",
    "source": "https://nautilustrader.io/docs/nightly/tutorials/backtest_fx_bars/",
}


def signal(ind, pos, htf=None):
    """EMA5 vs EMA20 golden/death cross."""
    f = ind["ema5"][pos]
    f1 = ind["ema5"][pos - 1]
    s = ind["ema20"][pos]
    s1 = ind["ema20"][pos - 1]
    if nan(f, f1, s, s1):
        return None
    if _xup(f, f1, s, s1):
        return "long"
    if _xdn(f, f1, s, s1):
        return "short"
    return None
