#!/usr/bin/env python3
"""williams_r_ob_os -- Williams %R simple OB/OS level entry. AlgoTest Pine / Larry Williams.

Long when willr < -80 (oversold). Short when willr > -20 (overbought).
Pure level trigger; ema200 trend filter added to reduce counter-trend entries.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "williams_r_ob_os",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "willr, ema200, close",
    "long": "willr < -80 AND close > ema200 (oversold in uptrend)",
    "short": "willr > -20 AND close < ema200 (overbought in downtrend)",
    "desc": "Williams %R OB/OS zone entry with EMA200 trend filter",
    "source": "web:https://docs.algotest.in/signals/pinescripts/williams_modr_strategy/",
}


def signal(ind, pos, htf=None):
    """Williams %R OB/OS with EMA200 trend direction filter."""
    wr = ind["willr"][pos]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(wr, c, e200):
        return None
    if wr < -80 and c > e200:
        return "long"
    if wr > -20 and c < e200:
        return "short"
    return None
