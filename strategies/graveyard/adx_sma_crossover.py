#!/usr/bin/env python3
"""adx_sma_crossover -- ADX SMA Crossover (AdxSmas freqtrade).
web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/AdxSmas.py
"""
from strategies._common import nan, _xup, TREND, ALL_CLASSES

META = {
    "id": "adx_sma_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "adx, sma10, sma20",
    "long": "ADX > 25 AND sma10 crosses above sma20 (substituting sma3/sma6 with closest available)",
    "short": "not implemented",
    "desc": "ADX-gated SMA crossover (ADX>25 for strength; sma10 x sma20 for direction)",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/AdxSmas.py",
}


def signal(ind, pos, htf=None):
    """Long only: ADX > 25 and sma10 crosses above sma20 (approx for sma3/sma6)."""
    adx = ind["adx"][pos]
    s10 = ind["sma10"][pos]
    s20 = ind["sma20"][pos]
    s10_1 = ind["sma10"][pos - 1]
    s20_1 = ind["sma20"][pos - 1]
    if nan(adx, s10, s20, s10_1, s20_1):
        return None
    if adx > 25 and _xup(s10, s10_1, s20, s20_1):
        return "long"
    return None
