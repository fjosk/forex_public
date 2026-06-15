#!/usr/bin/env python3
"""moving_average_direction_trend_system -- SMA50 slope direction: long when MA turns up, short when turns down; always-in reversal. alpha_trading_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "moving_average_direction_trend_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma50",
    "long": "SMA50 turns UP (current value > prior value)",
    "short": "SMA50 turns DOWN (current value < prior value)",
    "desc": "MA direction trend system: trade the sign of the SMA slope, always-in-market",
    "source": "book:alpha_trading_profitable_strategies_that_remove_di Ch 1-2",
}


def signal(ind, pos, htf=None):
    """Long on first bar SMA50 rises; short on first bar SMA50 falls."""
    if pos < 1:
        return None
    sma = ind["sma50"][pos]
    sma1 = ind["sma50"][pos - 1]
    if nan(sma, sma1):
        return None
    if sma > sma1:
        return "long"
    if sma < sma1:
        return "short"
    return None
