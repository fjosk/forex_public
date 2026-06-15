#!/usr/bin/env python3
"""price_vs_ma_trend_definition -- Price above/below a single MA defines trend bias. currency_trading_for_dummies_2nd_edition_by_brian.

TREND_FLIP: reverse when price crosses to the other side of the MA.
Uses EMA(50) as the representative period (closest available to 55-day, a common FX choice).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "price_vs_moving_average_trend_definition",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close,ema50",
    "long": "close crosses above EMA(50) -> uptrend bias long",
    "short": "close crosses below EMA(50) -> downtrend bias short",
    "desc": "Price vs single MA trend definition: uptrend when above EMA50, downtrend when below",
    "source": "currency_trading_for_dummies_2nd_edition_by_brian Ch11",
}


def signal(ind, pos, htf=None):
    """Cross of close above/below EMA50 defines trend direction."""
    if pos < 1:
        return None
    c  = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    e  = ind["ema50"][pos]
    e1 = ind["ema50"][pos - 1]
    if nan(c, c1, e, e1):
        return None
    # crossover triggers
    if c > e and c1 <= e1:
        return "long"
    if c < e and c1 >= e1:
        return "short"
    return None
