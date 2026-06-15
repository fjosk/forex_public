#!/usr/bin/env python3
"""wavetrend_oscillator -- WaveTrend WT1/WT2 cross in extreme zones. LazyBear / tradingview.com."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "wavetrend_oscillator",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h",
    "indicators": "wt1, wt2",
    "long": "wt1 crosses above wt2 while wt2 < -60 (oversold)",
    "short": "wt1 crosses below wt2 while wt2 > 60 (overbought)",
    "desc": "WaveTrend Oscillator: WT1/WT2 crossover in extreme zones",
    "source": "web:https://www.tradingview.com/script/2KE8wTuF-Indicator-WaveTrend-Oscillator-WT/",
}


def signal(ind, pos, htf=None):
    """WT1 cross above/below WT2 in oversold/overbought zone."""
    w1 = ind["wt1"][pos]
    w2 = ind["wt2"][pos]
    w1p = ind["wt1"][pos - 1]
    w2p = ind["wt2"][pos - 1]
    if nan(w1, w2, w1p, w2p):
        return None
    if _xup(w1, w1p, w2, w2p) and w2 < -60:
        return "long"
    if _xdn(w1, w1p, w2, w2p) and w2 > 60:
        return "short"
    return None
