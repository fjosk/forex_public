#!/usr/bin/env python3
"""swing_high_cci_rsi -- CCI deeply negative + RSI permissive: oversold swing entry (freqtrade SwingHighToSky).

Uses available cci and rsi (period 14); thresholds rescaled from the hyperopt-tuned 72/36-period versions.
No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "swing_high_cci_rsi",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "cci, rsi",
    "long": "cci < -100 AND rsi < 60 (oversold CCI with permissive RSI floor)",
    "short": "not implemented (long-only source strategy)",
    "desc": "Swing oversold entry: deep CCI negative + permissive RSI threshold; long-only",
    "source": "github.com/freqtrade/freqtrade-strategies SwingHighToSky.py (hyperopt-tuned CCI+RSI)",
}


def signal(ind, pos, htf=None):
    """Deep CCI oversold + RSI permissive: long-only swing entry."""
    cc = ind["cci"][pos]
    rs = ind["rsi"][pos]
    if nan(cc, rs):
        return None
    # Rescaled from CCI-72<-175 / RSI-36<90 to CCI-14<-100 / RSI-14<60
    if cc < -100 and rs < 60:
        return "long"
    return None
