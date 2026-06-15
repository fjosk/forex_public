#!/usr/bin/env python3
"""parabolic_sar_ema -- Parabolic SAR flip confirmed by EMA(8)/EMA(20) crossover. web:tradingpedia.com.

PSAR dot-flip as entry trigger, confirmed by EMA8 crossing EMA20 in the same direction.
No volume dependency. FX-applicable.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_ema",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "psar_dir, ema8, ema20",
    "long": "EMA8 crosses above EMA20 AND psar_dir == 1 (dot below price)",
    "short": "EMA8 crosses below EMA20 AND psar_dir == -1 (dot above price)",
    "desc": "Parabolic SAR flip confirmed by EMA8/EMA20 crossover",
    "source": "web:https://www.tradingpedia.com/forex-trading-strategies/forex-trading-strategy-9-combining-exponential-moving-average-and-parabolic-sar/",
}


def signal(ind, pos, htf=None):
    """PSAR flip entry confirmed by EMA8/EMA20 cross."""
    e8, e8p = ind["ema8"][pos], ind["ema8"][pos - 1]
    e20, e20p = ind["ema20"][pos], ind["ema20"][pos - 1]
    pdir = ind["psar_dir"][pos]
    pdirp = ind["psar_dir"][pos - 1]
    if nan(e8, e8p, e20, e20p, pdir, pdirp):
        return None
    if _xup(e8, e8p, e20, e20p) and pdir == 1:
        return "long"
    if _xdn(e8, e8p, e20, e20p) and pdir == -1:
        return "short"
    return None
