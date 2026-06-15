#!/usr/bin/env python3
"""sma10_sma20_crossover -- SMA(10) crosses above SMA(20) for long; below for short.
day_trading_swing_trading_the_currency_market_tech Ch.1 Figure 1.1.

Classic dual-MA crossover on daily bars. Example cited: 10/20 cross on GBP/USD.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "sma10_sma20_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "sma10,sma20",
    "long": "SMA(10) crosses above SMA(20)",
    "short": "SMA(10) crosses below SMA(20)",
    "desc": "10/20 SMA crossover: fast line crosses slow line to identify trend direction",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch.1 Perfect Market for Technical Analysis Figure 1.1",
}


def signal(ind, pos, htf=None):
    """SMA(10)/SMA(20) golden/death cross."""
    if pos < 1:
        return None
    f  = ind["sma10"][pos]
    s  = ind["sma20"][pos]
    f1 = ind["sma10"][pos - 1]
    s1 = ind["sma20"][pos - 1]
    if nan(f, s, f1, s1):
        return None
    if f > s and f1 <= s1:
        return "long"
    if f < s and f1 >= s1:
        return "short"
    return None
