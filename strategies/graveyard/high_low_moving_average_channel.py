#!/usr/bin/env python3
"""high_low_moving_average_channel -- EMA-of-highs / EMA-of-lows 13-period channel; buy near lower, sell near upper. elder_alexander_trading_for_a_living."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "high_low_moving_average_channel",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema_hi13, ema_lo13, close",
    "long": "Close touches or crosses below EMA-of-lows (buy near lower channel line)",
    "short": "Close touches or crosses above EMA-of-highs (sell near upper channel line)",
    "desc": "High/Low MA channel: 13-period EMA of highs and lows define a channel; trade at the band extremes",
    "source": "book:elder_alexander_trading_for_a_living Sec 45 p.253",
}


def signal(ind, pos, htf=None):
    """Entry at channel boundaries: long near lower (EMA lows), short near upper (EMA highs)."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    upper = ind["ema_hi13"][pos]
    lower = ind["ema_lo13"][pos]
    if nan(c, c1, upper, lower):
        return None
    # Long: price crosses from above lower line to at/below it
    if c <= lower and c1 > lower:
        return "long"
    # Short: price crosses from below upper line to at/above it
    if c >= upper and c1 < upper:
        return "short"
    return None
