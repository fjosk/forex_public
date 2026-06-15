#!/usr/bin/env python3
"""ga_chromosome_1_buy_on_strength_ma_below_close_stochastic_above_50 -- GA Chromosome 1: SMA(10) below prior close AND Stochastic(5) %K above 50 -> buy on strength (momentum). Kaufman.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ga_chromosome_1_buy_on_strength_ma_below_close_stochastic_above_50",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "sma10, stoch_k, close",
    "long": "SMA(10) < close[pos-1] AND Stochastic %K > 50",
    "short": "SMA(10) > close[pos-1] AND Stochastic %K < 50",
    "desc": "Genetic algorithm chromosome: buy on strength when MA below prior close and stochastic above midline",
    "source": "Kaufman, Trading Systems and Methods, Ch.20 Genetic Algorithms, p.499-500",
}


def signal(ind, pos, htf=None):
    """Buy on strength: MA below prior close and stochastic above 50."""
    if pos < 1:
        return None
    s10 = ind["sma10"][pos]
    sk = ind["stoch_k"][pos]
    c1 = ind["close"][pos - 1]
    if nan(s10, sk, c1):
        return None
    if s10 < c1 and sk > 50:
        return "long"
    if s10 > c1 and sk < 50:
        return "short"
    return None
