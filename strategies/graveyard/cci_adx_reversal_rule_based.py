#!/usr/bin/env python3
"""cci_adx_reversal_rule_based -- CCI cross +/-100 in weak-trend regime (ADX<25). armelf Financial-Algorithms.

No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "cci_adx_reversal_rule_based",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1d",
    "indicators": "cci, adx, di_plus, di_minus",
    "long": "downtrend (di_minus>di_plus) AND ADX<25 (weak) AND CCI crosses above +100",
    "short": "uptrend (di_plus>di_minus) AND ADX<25 (weak) AND CCI crosses below -100",
    "desc": "CCI+ADX reversal: counter-trend CCI cross at exhausted trend (ADX weak)",
    "source": "github.com/armelf/Financial-Algorithms CCI ADX Reversal Strategy",
}

_ADX_WEAK = 25.0
_CCI_THRESH = 100.0


def signal(ind, pos, htf=None):
    """CCI cross of +/-100 in weak ADX trend environment."""
    if pos < 1:
        return None
    cc0 = ind["cci"][pos]
    cc1 = ind["cci"][pos - 1]
    dx = ind["adx"][pos]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    if nan(cc0, cc1, dx, dip, dim):
        return None
    weak = dx < _ADX_WEAK
    if not weak:
        return None
    downtrend = dim > dip
    uptrend = dip > dim
    # Long: downtrend exhausting, CCI crosses above +100
    if downtrend and cc0 > _CCI_THRESH and cc1 <= _CCI_THRESH:
        return "long"
    # Short: uptrend exhausting, CCI crosses below -100
    if uptrend and cc0 < -_CCI_THRESH and cc1 >= -_CCI_THRESH:
        return "short"
    return None
