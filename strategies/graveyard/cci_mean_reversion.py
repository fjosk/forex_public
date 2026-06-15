#!/usr/bin/env python3
"""cci_mean_reversion -- CCI Commodity Channel Index mean reversion. Donald Lambert / QuantifiedStrategies.

CCI crosses above -100 from below (exit oversold) -> long.
CCI crosses below +100 from above (exit overbought) -> short.
Optional SMA200 trend filter to only fade against the trend.
Source: web:https://www.quantifiedstrategies.com/cci-trading-strategy/
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "cci_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "cci, sma200, close",
    "long": "CCI crosses above -100 from below (exit oversold)",
    "short": "CCI crosses below +100 from above (exit overbought)",
    "desc": "CCI mean reversion: -100/+100 threshold crossover entries",
    "source": "web:https://www.quantifiedstrategies.com/cci-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """CCI cross above -100 (long) or below +100 (short)."""
    if pos < 1:
        return None
    cci = ind["cci"][pos]
    cci1 = ind["cci"][pos - 1]
    if nan(cci, cci1):
        return None

    # Long: cross above -100 from below
    if _xup(cci, cci1, -100.0, -100.0):
        return "long"

    # Short: cross below +100 from above
    if _xdn(cci, cci1, 100.0, 100.0):
        return "short"

    return None
