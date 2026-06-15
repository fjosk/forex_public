#!/usr/bin/env python3
"""moving_average_crossover_mechanical_system_price_vs_ma -- Price above/below MA AND MA slope both required; classic Elder mechanical MA system. elder_alexander_trading_for_a_living."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "moving_average_crossover_mechanical_system_price_vs_ma",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close, ema20",
    "long": "Close above EMA20 AND EMA20 is rising",
    "short": "Close below EMA20 AND EMA20 is falling",
    "desc": "Elder mechanical MA system: price above/below MA with MA slope confirmation",
    "source": "book:elder_alexander_trading_for_a_living Sec 25 p.125",
}


def signal(ind, pos, htf=None):
    """Long when close above rising EMA; short when close below falling EMA."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    ema = ind["ema20"][pos]
    ema1 = ind["ema20"][pos - 1]
    if nan(c, ema, ema1):
        return None
    if c > ema and ema > ema1:
        return "long"
    if c < ema and ema < ema1:
        return "short"
    return None
