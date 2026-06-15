#!/usr/bin/env python3
"""sar_stochastic_trend_filter -- Parabolic SAR + Stochastic Trend-Filtered Entry.
web:https://github.com/armelf/Financial-Algorithms
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "sar_stochastic_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "psar_dir, stoch_k, di_plus, di_minus",
    "long": "DI+ > DI- AND SAR below price (psar_dir=1) AND stoch_k crosses above 20",
    "short": "DI- > DI+ AND SAR above price (psar_dir=-1) AND stoch_k crosses below 80",
    "desc": "Parabolic SAR direction + Stochastic threshold cross filtered by DI trend",
    "source": "web:https://github.com/armelf/Financial-Algorithms",
}


def signal(ind, pos, htf=None):
    """SAR trend direction + stochastic oversold/overbought cross in DI-confirmed trend."""
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    psd = ind["psar_dir"][pos]
    if nan(sk, sk1, dip, dim, psd):
        return None
    uptrend = dip > dim
    downtrend = dim > dip
    sar_bull = psd == 1
    sar_bear = psd == -1
    # stoch crosses above 20 (exit oversold)
    stoch_xup20 = sk > 20 and sk1 <= 20
    # stoch crosses below 80 (exit overbought)
    stoch_xdn80 = sk < 80 and sk1 >= 80
    if uptrend and sar_bull and stoch_xup20:
        return "long"
    if downtrend and sar_bear and stoch_xdn80:
        return "short"
    return None
