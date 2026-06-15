#!/usr/bin/env python3
"""cci_trend_breakout -- CCI Trend-Mode Breakout. mql5 articles 10592.

Trending market: CCI crossing above +100 = long (momentum breakout into upper zone).
CCI crossing below -100 = short. Regime detected by chop (chop < 50 = trending).
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "cci_trend_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "cci, chop",
    "long": "chop < 50 (trending) AND cci crosses above +100",
    "short": "chop < 50 (trending) AND cci crosses below -100",
    "desc": "CCI +/-100 breakout in trending regime (chop < 50); trend-mode variant",
    "source": "web:https://www.mql5.com/en/articles/10592",
}


def signal(ind, pos, htf=None):
    """CCI breakout above +100 / below -100 in trending market."""
    cc = ind["cci"][pos]
    cc1 = ind["cci"][pos - 1]
    ch = ind["chop"][pos]
    if nan(cc, cc1, ch):
        return None
    trending = ch < 50
    if trending and _xup(cc, cc1, 100.0, 100.0):
        return "long"
    if trending and _xdn(cc, cc1, -100.0, -100.0):
        return "short"
    return None
