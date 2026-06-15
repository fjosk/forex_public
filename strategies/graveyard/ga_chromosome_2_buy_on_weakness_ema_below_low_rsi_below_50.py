#!/usr/bin/env python3
"""ga_chromosome_2_buy_on_weakness_ema_below_low_rsi_below_50 -- Genetic-algorithm chromosome 2:
buy when EMA20 < prior low AND RSI < 50; short when EMA20 > prior high AND RSI > 50.

Source: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch.20 p.499-500.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "ga_chromosome_2_buy_on_weakness_ema_below_low_rsi_below_50",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "ema20, rsi, low, high",
    "long": "EMA20 < low[1] (prior bar low) AND RSI < 50 (weakness with below-neutral momentum)",
    "short": "EMA20 > high[1] (prior bar high) AND RSI > 50 (strength with above-neutral momentum)",
    "desc": "GA chromosome 2: buy on weakness (EMA below prior low + RSI sub-50); mirror short",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.20 pp.499-500",
}


def signal(ind, pos, htf=None):
    """Buy when EMA20 < prior low and RSI < 50; short when EMA20 > prior high and RSI > 50."""
    if pos < 1:
        return None
    e = ind["ema20"][pos]
    r = ind["rsi"][pos]
    lo1 = ind["low"][pos - 1]
    hi1 = ind["high"][pos - 1]
    if nan(e, r, lo1, hi1):
        return None
    if e < lo1 and r < 50:
        return "long"
    if e > hi1 and r > 50:
        return "short"
    return None
