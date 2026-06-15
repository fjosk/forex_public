#!/usr/bin/env python3
"""cci_wma_scalp -- CCI + WMA Scalp. hasnocool/tradingview-pine-scripts.

Price above sma20 (proxy for WMA20, volume-weighted excluded) + CCI crosses above -100 = long.
Price below sma20 + CCI crosses below +100 = short.
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "cci_wma_scalp",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "5m",
    "indicators": "cci, sma20, close",
    "long": "close > sma20 AND cci crosses above -100",
    "short": "close < sma20 AND cci crosses below +100",
    "desc": "CCI -100/+100 cross with price above/below SMA20 MA filter (WMA20 approximation)",
    "source": "web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/CCI%20Scalping%20Strategy.pine",
}


def signal(ind, pos, htf=None):
    """CCI cross of -100/+100 with SMA20 trend filter."""
    cc = ind["cci"][pos]
    cc1 = ind["cci"][pos - 1]
    s20 = ind["sma20"][pos]
    c = ind["close"][pos]
    if nan(cc, cc1, s20, c):
        return None
    if c > s20 and _xup(cc, cc1, -100.0, -100.0):
        return "long"
    if c < s20 and _xdn(cc, cc1, 100.0, 100.0):
        return "short"
    return None
