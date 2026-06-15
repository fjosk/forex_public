#!/usr/bin/env python3
"""universal_macd_ratio -- Universal MACD Ratio Band (uMACD).
web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/UniversalMACD.py
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "universal_macd_ratio",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "ema13, ema20",
    "long": "umacd = ema13/ema20 - 1 is in the narrow band [-0.01416, -0.01176]",
    "short": "not implemented (long-only strategy)",
    "desc": "MACD-ratio band entry: EMA13/EMA20 - 1 enters a hyperopt-tuned negative window",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/UniversalMACD.py",
}

# Hyperopt-tuned thresholds from original freqtrade strategy
_BUY_LO = -0.01416
_BUY_HI = -0.01176


def signal(ind, pos, htf=None):
    """uMACD = ema13/ema20 - 1; enter long when it falls in the tuned negative window."""
    e13 = ind["ema13"][pos]
    e20 = ind["ema20"][pos]
    if nan(e13, e20) or e20 == 0:
        return None
    umacd = (e13 / e20) - 1.0
    if _BUY_LO <= umacd <= _BUY_HI:
        return "long"
    return None
