#!/usr/bin/env python3
"""krausz_hilo_activator_breakout -- Close above SMA(high, n) = long; close below SMA(low, n) = short. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "krausz_hilo_activator_moving_average_of_highs_lows_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "sma_high21, sma_low21, close",
    "long": "close crosses above SMA of bar highs (HiLo Activator buy line)",
    "short": "close crosses below SMA of bar lows (HiLo Activator sell line)",
    "desc": "Krausz HiLo Activator: close vs SMA-of-highs / SMA-of-lows stop-and-reverse breakout",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Close above SMA(high,21) = long; close below SMA(low,21) = short."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    buy_line = ind["sma_high21"][pos]
    sell_line = ind["sma_low21"][pos]
    if nan(c, buy_line, sell_line):
        return None
    if c > buy_line:
        return "long"
    if c < sell_line:
        return "short"
    return None
