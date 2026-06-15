#!/usr/bin/env python3
"""sma200_price_filter -- Hold long while price is above the 200-day SMA; exit to flat (no
short) when price closes below. the_new_market_wizards Sperandeo interview.

Cited result: ~18% avg annual return on Dow stocks over 50 years, roughly double buy-and-hold.
Adapted here as a long/short filter: long above SMA200, short below SMA200 (trend extension).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "sma200_price_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "close,sma200",
    "long": "close crosses above SMA(200) - price enters uptrend regime",
    "short": "close crosses below SMA(200) - price enters downtrend regime",
    "desc": "200-day SMA price filter: long above the 200-day MA, short below (trend regime filter)",
    "source": "the_new_market_wizards Sperandeo interview 200-day moving average p.106",
}


def signal(ind, pos, htf=None):
    """Long/short based on price side of the 200-bar SMA."""
    if pos < 1:
        return None
    c    = ind["close"][pos]
    c1   = ind["close"][pos - 1]
    s200 = ind["sma200"][pos]
    s2001 = ind["sma200"][pos - 1]
    if nan(c, c1, s200, s2001):
        return None
    # Cross above SMA200
    if c > s200 and c1 <= s2001:
        return "long"
    # Cross below SMA200
    if c < s200 and c1 >= s2001:
        return "short"
    return None
