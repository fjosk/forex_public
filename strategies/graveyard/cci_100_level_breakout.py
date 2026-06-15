#!/usr/bin/env python3
"""cci_100_level_breakout -- CCI crosses +100/-100 trend breakout (Lambert rule). web:stockcharts."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "cci_100_level_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "cci, atr",
    "long": "CCI(20) crosses above +100 from below",
    "short": "CCI(20) crosses below -100 from above",
    "desc": "CCI +100/-100 Lambert trend breakout: cross above +100 is long, below -100 is short",
    "source": "web:https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/commodity-channel-index-cci",
}

_LEVEL = 100.0


def signal(ind, pos, htf=None):
    """CCI +100/-100 level crossover breakout."""
    cci = ind["cci"][pos]
    cci1 = ind["cci"][pos - 1]
    if nan(cci, cci1):
        return None
    if _xup(cci, cci1, _LEVEL, _LEVEL):
        return "long"
    if _xdn(cci, cci1, -_LEVEL, -_LEVEL):
        return "short"
    return None
