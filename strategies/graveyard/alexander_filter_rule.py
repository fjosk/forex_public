#!/usr/bin/env python3
"""alexander_filter_rule -- Alexander's x% filter rule: price rises/falls x% from recent swing extreme. trading_systems_and_methods_kaufman_perry_j_kaufma.

Long when close rises >= x% above the lowest recent Donchian low (proxy for swing low).
Short when close falls >= x% below the highest recent Donchian high (proxy for swing high).
x = 1% filter (1.0/100 = 0.01).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "alexander_filter_rule",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,dc_up,dc_lo",
    "long": "close >= dc_lo * (1 + 0.01): price rose 1% above Donchian low (swing low proxy)",
    "short": "close <= dc_up * (1 - 0.01): price fell 1% below Donchian high (swing high proxy)",
    "desc": "Alexander filter rule: 1% price reversal from recent Donchian extreme generates trend signal",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma, Ch21 Table21-12",
}

_FILTER = 0.01  # 1% filter


def signal(ind, pos, htf=None):
    """Alexander x% filter rule using Donchian extremes as swing proxies."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]  # prior period's Donchian high
    dc_lo = ind["dc_lo"][pos - 1]  # prior period's Donchian low
    if nan(c, dc_up, dc_lo) or dc_lo <= 0 or dc_up <= 0:
        return None
    if c >= dc_lo * (1.0 + _FILTER):
        return "long"
    if c <= dc_up * (1.0 - _FILTER):
        return "short"
    return None
