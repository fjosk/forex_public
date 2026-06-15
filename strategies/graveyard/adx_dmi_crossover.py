#!/usr/bin/env python3
"""adx_dmi_crossover -- ADX trend gate + DI crossover entry. AvaTrade."""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "adx_dmi_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h/daily",
    "indicators": "adx, di_plus, di_minus",
    "long": "+DI crosses above -DI AND ADX > 25",
    "short": "-DI crosses above +DI AND ADX > 25",
    "desc": "ADX/DMI crossover: DI directional cross gated by ADX trend strength",
    "source": "web:https://www.avatrade.com/education/technical-analysis-indicators-strategies/adx-indicator-trading-strategies",
}


def signal(ind, pos, htf=None):
    """DI crossover with ADX > 25 trend gate."""
    if pos < 1:
        return None
    adx = ind["adx"][pos]
    dp0 = ind["di_plus"][pos]
    dm0 = ind["di_minus"][pos]
    dp1 = ind["di_plus"][pos - 1]
    dm1 = ind["di_minus"][pos - 1]
    if nan(adx, dp0, dm0, dp1, dm1):
        return None

    trending = adx > 25

    if trending and _xup(dp0, dp1, dm0, dm1):
        return "long"
    if trending and _xdn(dp0, dp1, dm0, dm1):
        return "short"

    return None
