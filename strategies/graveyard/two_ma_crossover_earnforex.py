#!/usr/bin/env python3
"""two_ma_crossover_earnforex -- Dual SMA10/50 crossover EA. EarnForex 2 MA Crossover (MQL4)."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "two_ma_crossover_earnforex",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "sma10, sma50",
    "long": "sma10 crosses above sma50 (golden cross)",
    "short": "sma10 crosses below sma50 (death cross)",
    "desc": "EarnForex dual SMA crossover EA: SMA10/50 golden/death cross with reversal exit",
    "source": "EarnForex 2 MA Crossover EA (MQL4); earnforex.com/metatrader-expert-advisors/2-ma-crossover/",
}


def signal(ind, pos, htf=None):
    """SMA10/50 crossover entry."""
    f = ind["sma10"][pos]
    s = ind["sma50"][pos]
    f1 = ind["sma10"][pos - 1]
    s1 = ind["sma50"][pos - 1]
    if nan(f, s, f1, s1):
        return None
    if _xup(f, f1, s, s1):
        return "long"
    if _xdn(f, f1, s, s1):
        return "short"
    return None
