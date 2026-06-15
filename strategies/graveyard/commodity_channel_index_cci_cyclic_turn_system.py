#!/usr/bin/env python3
"""commodity_channel_index_cci_cyclic_turn_system -- Lambert CCI cyclic turn system: long on CCI cross above +100, short on cross below -100. trading_systems_and_methods_kaufman_perry_j_kaufma Ch8."""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "commodity_channel_index_cci_cyclic_turn_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "cci",
    "long": "CCI crosses above +100 (cyclic turn upward)",
    "short": "CCI crosses below -100 (cyclic turn downward)",
    "desc": "Lambert CCI cyclic turn system: breakout above +100 long, breakdown below -100 short",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch8",
}


def signal(ind, pos, htf=None):
    """Long on CCI cross above +100; short on CCI cross below -100."""
    if pos < 1:
        return None
    cc = ind["cci"][pos]
    cc1 = ind["cci"][pos - 1]
    if nan(cc, cc1):
        return None
    if _xup(cc, cc1, 100.0, 100.0):
        return "long"
    if _xdn(cc, cc1, -100.0, -100.0):
        return "short"
    return None
