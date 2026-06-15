#!/usr/bin/env python3
"""adx_dmi_trend_entry_swing -- ADX > 25 trend gate + DI cross swing entry. FxNX."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "adx_dmi_trend_entry_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "adx, di_plus, di_minus",
    "long": "ADX > 25 AND +DI crosses above -DI",
    "short": "ADX > 25 AND -DI crosses above +DI",
    "desc": "ADX + DMI swing: trend-strength gate plus directional crossover entry",
    "source": "web:https://fxnx.com/en/blog/adx-indicator-strategy-the-gatekeeper-to-profitable-trends",
}


def signal(ind, pos, htf=None):
    """ADX-gated DI crossover with trend-following exit envelope."""
    if pos < 1:
        return None
    adx = ind["adx"][pos]
    dp0 = ind["di_plus"][pos]
    dm0 = ind["di_minus"][pos]
    dp1 = ind["di_plus"][pos - 1]
    dm1 = ind["di_minus"][pos - 1]
    if nan(adx, dp0, dm0, dp1, dm1):
        return None

    if adx > 25 and _xup(dp0, dp1, dm0, dm1):
        return "long"
    if adx > 25 and _xdn(dp0, dp1, dm0, dm1):
        return "short"

    return None
