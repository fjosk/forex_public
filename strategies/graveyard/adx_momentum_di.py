#!/usr/bin/env python3
"""adx_momentum_di -- ADX Momentum DI Trend Filter (ADXMomentum freqtrade).
web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/ADXMomentum.py
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_momentum_di",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "adx, di_plus, di_minus, roc",
    "long": "ADX>25 AND roc>0 (momentum) AND di_plus>25 AND di_plus>di_minus",
    "short": "not implemented",
    "desc": "ADXMomentum: ADX strength + positive ROC momentum + DI directional confirm for long only",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/ADXMomentum.py",
}


def signal(ind, pos, htf=None):
    """Long only: ADX > 25, ROC > 0, DI+ > 25, DI+ > DI-."""
    adx = ind["adx"][pos]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    roc = ind["roc"][pos]
    if nan(adx, dip, dim, roc):
        return None
    if adx > 25 and roc > 0 and dip > 25 and dip > dim:
        return "long"
    return None
