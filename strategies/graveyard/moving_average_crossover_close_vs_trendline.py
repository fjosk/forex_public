#!/usr/bin/env python3
"""moving_average_crossover_close_vs_trendline -- Close crosses above/below SMA20 (price vs trendline crossover). trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "moving_average_crossover_close_vs_trendline",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close, sma20",
    "long": "Close crosses above SMA20 (price penetrates trendline upward)",
    "short": "Close crosses below SMA20 (price penetrates trendline downward)",
    "desc": "Basic price vs MA crossover: close crossing the moving average trendline",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma Ch5 Basic Buy/Sell",
}


def signal(ind, pos, htf=None):
    """Close crosses SMA20 for trend reversal entry."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    sma = ind["sma20"][pos]
    sma1 = ind["sma20"][pos - 1]
    if nan(c, c1, sma, sma1):
        return None
    if _xup(c, c1, sma, sma1):
        return "long"
    if _xdn(c, c1, sma, sma1):
        return "short"
    return None
