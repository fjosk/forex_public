#!/usr/bin/env python3
"""one_year_moving_average_crossover_long_term_trend_filter -- Price crosses above/below SMA200 (~1-year) for long-term trend entry. trade_your_way_to_financial_freedom."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "one_year_moving_average_crossover_long_term_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close, sma200",
    "long": "Close crosses above SMA200 (one-year moving average)",
    "short": "Close crosses below SMA200",
    "desc": "One-year MA crossover: long when price crosses above SMA200, short when below",
    "source": "book:trade_your_way_to_financial_freedom_mabroke_blogsp Ch 8 Colby-Meyers",
}


def signal(ind, pos, htf=None):
    """Close crosses SMA200 for long-term trend reversal entry."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    sma = ind["sma200"][pos]
    sma1 = ind["sma200"][pos - 1]
    if nan(c, c1, sma, sma1):
        return None
    if _xup(c, c1, sma, sma1):
        return "long"
    if _xdn(c, c1, sma, sma1):
        return "short"
    return None
