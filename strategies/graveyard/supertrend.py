#!/usr/bin/env python3
"""supertrend -- SuperTrend ATR-band flip. web:fxempire.com.

st_dir changes from -1 to +1 = long; from +1 to -1 = short. The standard ATR-centered
trailing band reversal. Baseline variant; no additional filters.
No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir, st_line",
    "long": "st_dir flips from -1 to +1 (close crosses above SuperTrend line)",
    "short": "st_dir flips from +1 to -1 (close crosses below SuperTrend line)",
    "desc": "SuperTrend ATR-band direction flip (baseline)",
    "source": "web:https://www.fxempire.com/forecasts/article/supertrend-indicator-explained-formula-trading-strategy-pros-cons-1598359",
}


def signal(ind, pos, htf=None):
    """SuperTrend flip -- baseline version."""
    sd = ind["st_dir"][pos]
    sdp = ind["st_dir"][pos - 1]
    if nan(sd, sdp):
        return None
    if sd == 1 and sdp == -1:
        return "long"
    if sd == -1 and sdp == 1:
        return "short"
    return None
