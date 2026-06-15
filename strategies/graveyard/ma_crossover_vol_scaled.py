#!/usr/bin/env python3
"""ma_crossover_vol_scaled -- EMA50/SMA200 golden-death cross, volatility-scaled. Medium/QuantStart.

Buy when EMA50 crosses above SMA200 (golden cross), sell when it crosses below (death cross).
Position sizing is inversely proportional to realized volatility (atr_pct proxy), but signal
direction is the primary output; the engine handles sizing.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ma_crossover_vol_scaled",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "ema50, sma200, atr_pct",
    "long": "EMA50 crosses above SMA200 (golden cross)",
    "short": "EMA50 crosses below SMA200 (death cross)",
    "desc": "EMA50/SMA200 crossover with inverse-volatility position sizing",
    "source": "web:https://medium.com/@jpolec_72972/quantitative-strategy-analysis-volatility-scaled-moving-average-crossover-08980aec12e5",
}


def signal(ind, pos, htf=None):
    """EMA50/SMA200 crossover signal."""
    e50 = ind["ema50"][pos]
    s200 = ind["sma200"][pos]
    e50_1 = ind["ema50"][pos - 1]
    s200_1 = ind["sma200"][pos - 1]
    atr_p = ind["atr_pct"][pos]
    if nan(e50, s200, e50_1, s200_1, atr_p):
        return None
    if _xup(e50, e50_1, s200, s200_1):
        return "long"
    if _xdn(e50, e50_1, s200, s200_1):
        return "short"
    return None
