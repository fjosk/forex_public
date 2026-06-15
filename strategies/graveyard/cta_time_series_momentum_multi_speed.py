#!/usr/bin/env python3
"""cta_time_series_momentum_multi_speed -- CTA multi-speed TSMOM ensemble. CME/Moskowitz et al.

Combines 1m/3m/6m/12m return signals (each votes +1 or -1). Long if score >= 2; short if <= -2.
Flat in the neutral zone (-1, 0, +1). Managed-futures CTA standard approach.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "cta_time_series_momentum_multi_speed",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "close (20/60/120/250 bar lookbacks)",
    "long": "score >= 2: majority of 1m/3m/6m/12m lookbacks positive",
    "short": "score <= -2: majority of lookbacks negative",
    "desc": "CTA multi-speed TSMOM ensemble (1m/3m/6m/12m majority vote)",
    "source": "web:https://www.cmegroup.com/education/files/improving-time-series-momentum-strategies.pdf",
}

_LOOKBACKS = [20, 60, 120, 250]  # 1m, 3m, 6m, 12m in daily bars


def signal(ind, pos, htf=None):
    """Multi-lookback TSMOM vote."""
    max_lb = max(_LOOKBACKS)
    if pos < max_lb + 1:
        return None
    c = ind["close"][pos]
    if nan(c):
        return None
    score = 0
    for lb in _LOOKBACKS:
        c_back = ind["close"][pos - lb]
        if nan(c_back) or c_back == 0:
            return None
        ret = (c - c_back) / c_back
        score += 1 if ret > 0 else -1
    if score >= 2:
        return "long"
    if score <= -2:
        return "short"
    return None
