#!/usr/bin/env python3
"""heikin_ashi_trend_sequence -- Heikin-Ashi Three-Bar Trend Sequence. PyQuantLab HA."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "heikin_ashi_trend_sequence",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_close, ha_open, high, low",
    "long": "3 consecutive HA green candles with no lower wick (ha_open == ha_lo)",
    "short": "3 consecutive HA red candles with no upper wick (ha_open == ha_hi)",
    "desc": "Three consecutive full-body Heikin-Ashi candles with no reversal-side wick",
    "source": "pyquantlab.com Heikin-Ashi Trend-Following with Trailing Stops",
}

_TOL = 1e-10  # floating-point tolerance for wick == 0 check


def signal(ind, pos, htf=None):
    """Three-bar strong HA sequence: full body, no wick on reversal side."""
    hac = ind["ha_close"]
    hao = ind["ha_open"]
    hi = ind["high"]
    lo = ind["low"]
    if pos < 2:
        return None
    # check three bars
    for i in (pos - 2, pos - 1, pos):
        if nan(hac[i], hao[i], hi[i], lo[i]):
            return None
    def ha_lo(i):
        return min(lo[i], hao[i], hac[i])
    def ha_hi(i):
        return max(hi[i], hao[i], hac[i])
    def strong_green(i):
        return hac[i] > hao[i] and abs(hao[i] - ha_lo(i)) < _TOL
    def strong_red(i):
        return hac[i] < hao[i] and abs(hao[i] - ha_hi(i)) < _TOL
    if all(strong_green(i) for i in (pos - 2, pos - 1, pos)):
        return "long"
    if all(strong_red(i) for i in (pos - 2, pos - 1, pos)):
        return "short"
    return None
