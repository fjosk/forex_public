#!/usr/bin/env python3
"""heikin_ashi_momentum_trend -- N consecutive HA bars in same color = momentum trend signal. je-suis-tm."""
from strategies._common import nan, TREND, ALL_CLASSES

_N = 3  # consecutive HA bars required

META = {
    "id": "heikin_ashi_momentum_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ha_close, ha_open",
    "long": "N=3 consecutive bullish HA bars (ha_close > ha_open) after prior bearish sequence",
    "short": "N=3 consecutive bearish HA bars after prior bullish sequence",
    "desc": "Heikin-Ashi momentum: consecutive bar color sequence triggers trend entry",
    "source": "https://github.com/je-suis-tm/quant-trading",
}


def signal(ind, pos, htf=None):
    """N consecutive HA bars in same direction."""
    if pos < _N + 1:
        return None
    hc = ind["ha_close"]
    ho = ind["ha_open"]
    for i in range(_N):
        if nan(hc[pos - i], ho[pos - i]):
            return None
    if nan(hc[pos - _N], ho[pos - _N]):
        return None
    all_bull = all(hc[pos - i] > ho[pos - i] for i in range(_N))
    all_bear = all(hc[pos - i] < ho[pos - i] for i in range(_N))
    # previous bar (before the streak) must be opposite to confirm it's a new streak
    prev_was_bear = hc[pos - _N] < ho[pos - _N]
    prev_was_bull = hc[pos - _N] > ho[pos - _N]
    if all_bull and prev_was_bear:
        return "long"
    if all_bear and prev_was_bull:
        return "short"
    return None
