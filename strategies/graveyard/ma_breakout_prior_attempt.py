#!/usr/bin/env python3
"""ma_breakout_prior_attempt -- Price closes above SMA100 which acts as breakout trigger.
day_trading_swing_trading_the_currency_market_tech.
"""
from strategies._common import nan, _xup, _xdn, BREAK, ALL_CLASSES

META = {
    "id": "ma_breakout_prior_attempt",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "sma100",
    "long": "close crosses above SMA100",
    "short": "close crosses below SMA100",
    "desc": "Moving-average breakout: close crosses SMA100 for trend entry",
    "source": "book: day_trading_swing_trading_the_currency_market_tech",
}


def signal(ind, pos, htf=None):
    """Close crosses SMA100 from below (long) or above (short)."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    s = ind["sma100"][pos]
    s1 = ind["sma100"][pos - 1]
    if nan(c, c1, s, s1):
        return None
    if _xup(c, c1, s, s1):
        return "long"
    if _xdn(c, c1, s, s1):
        return "short"
    return None
