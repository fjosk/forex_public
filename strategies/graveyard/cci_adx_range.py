#!/usr/bin/env python3
"""cci_adx_range -- CCI Mean Reversion with ADX Range Filter. armelf/Financial-Algorithms.

ADX < 25 confirms ranging market. CCI dropping below 100 after being above = fade overbought (long).
CCI rising above -100 after being below = fade oversold (short).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "cci_adx_range",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1d",
    "indicators": "cci, adx",
    "long": "adx < 25 AND cci[pos-1] > 100 AND cci[pos] < 100 (CCI drops below overbought)",
    "short": "adx < 25 AND cci[pos-1] < -100 AND cci[pos] > -100 (CCI rises above oversold)",
    "desc": "CCI mean reversion gated by ADX ranging filter (<25); fade CCI +/-100 level breaks",
    "source": "web:https://github.com/armelf/Financial-Algorithms",
}


def signal(ind, pos, htf=None):
    """CCI overbought/oversold fade in ranging market (ADX < 25)."""
    cc = ind["cci"][pos]
    cc1 = ind["cci"][pos - 1]
    dx = ind["adx"][pos]
    if nan(cc, cc1, dx):
        return None
    if dx < 25 and cc1 > 100 and cc < 100:
        return "long"
    if dx < 25 and cc1 < -100 and cc > -100:
        return "short"
    return None
