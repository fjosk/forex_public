#!/usr/bin/env python3
"""cci_zero_cross -- CCI(14) zero-line cross with SMA200 trend filter. earnforex.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "cci_zero_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "cci, sma200",
    "long": "CCI crosses above 0 from below AND close > sma200",
    "short": "CCI crosses below 0 from above AND close < sma200",
    "desc": "CCI zero-line momentum cross with SMA200 trend direction filter",
    "source": "web:https://www.earnforex.com/guides/trading-strategies/",
}


def signal(ind, pos, htf=None):
    """CCI zero-line crossover aligned with SMA200 trend."""
    cc = ind["cci"][pos]
    ccp = ind["cci"][pos - 1]
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    if nan(cc, ccp, c, s200):
        return None
    cci_cross_up = cc > 0 and ccp <= 0
    cci_cross_dn = cc < 0 and ccp >= 0
    if cci_cross_up and c > s200:
        return "long"
    if cci_cross_dn and c < s200:
        return "short"
    return None
