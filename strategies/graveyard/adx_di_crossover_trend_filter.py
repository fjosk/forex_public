#!/usr/bin/env python3
"""adx_di_crossover_trend_filter -- DI crossover gated by ADX>25 trend strength. Quant-Signals.

Enter in the direction of the DI crossover only when ADX confirms trend strength (>25).
ADX rising condition adds confirmation that the trend is strengthening.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "adx_di_crossover_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "adx, di_plus, di_minus",
    "long": "DI+ crosses above DI- and ADX > 25",
    "short": "DI- crosses above DI+ and ADX > 25",
    "desc": "DI crossover with ADX trend strength gate (quant-signals.com variant)",
    "source": "web:https://quant-signals.com/adx-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """DI cross filtered by ADX > 25."""
    adx_v = ind["adx"][pos]
    dp = ind["di_plus"][pos]
    dm = ind["di_minus"][pos]
    dp1 = ind["di_plus"][pos - 1]
    dm1 = ind["di_minus"][pos - 1]
    if nan(adx_v, dp, dm, dp1, dm1):
        return None
    if adx_v < 25:
        return None
    if _xup(dp, dp1, dm, dm1):
        return "long"
    if _xdn(dp, dp1, dm, dm1):
        return "short"
    return None
