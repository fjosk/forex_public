#!/usr/bin/env python3
"""two_time_frame_stochastic_linear_regression_slope_trend_filter -- LR slope trend filter (HTF) + stochastic oversold/overbought entry (entry TF). Kaufman.

tier1 multi-timeframe. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "two_time_frame_stochastic_linear_regression_slope_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "lr_slope_price, stoch_k",
    "long": "LR slope > 0 (uptrend) AND stoch_k < 20 (oversold)",
    "short": "LR slope < 0 (downtrend) AND stoch_k > 80 (overbought)",
    "desc": "Kaufman dual-timeframe: LR slope trend filter + stochastic extreme entry",
    "source": "Kaufman, Trading Systems and Methods, Ch.19 Multiple Time Frames, Fig 19-1",
}


def signal(ind, pos, htf=None):
    """LR slope trend filter with stochastic extreme entry."""
    if pos < 1:
        return None
    slope = ind["lr_slope_price"][pos]
    sk = ind["stoch_k"][pos]
    if nan(slope, sk):
        return None
    if slope > 0 and sk < 20:
        return "long"
    if slope < 0 and sk > 80:
        return "short"
    return None
