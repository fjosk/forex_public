#!/usr/bin/env python3
"""cci_moving_average_filter -- CCI exits oversold/overbought zone with SMA100 trend filter. quantifiedstrategies.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "cci_moving_average_filter",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "cci, sma100",
    "long": "close > sma100 AND CCI crosses above -100 (exits oversold)",
    "short": "close < sma100 AND CCI crosses below +100 (exits overbought)",
    "desc": "CCI mean-reversion: exit from oversold/overbought with SMA100 trend direction filter",
    "source": "web:https://www.quantifiedstrategies.com/cci-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """CCI exits extreme zone while on the correct side of SMA100."""
    cc = ind["cci"][pos]
    ccp = ind["cci"][pos - 1]
    c = ind["close"][pos]
    s100 = ind["sma100"][pos]
    if nan(cc, ccp, c, s100):
        return None
    trend_up = c > s100
    trend_dn = c < s100
    # Exit oversold: CCI crosses above -100 from below
    cci_exit_os = cc > -100 and ccp <= -100
    # Exit overbought: CCI crosses below +100 from above
    cci_exit_ob = cc < 100 and ccp >= 100
    if trend_up and cci_exit_os:
        return "long"
    if trend_dn and cci_exit_ob:
        return "short"
    return None
