#!/usr/bin/env python3
"""triple_ema_crossover_3_13_144 -- Triple EMA 3/13/144 crossover system. web:strategy-workspaceegiesresources.com.

Fast EMA (ema5 proxies ema3) crosses ema13 in direction of ema144. All three must be
in perfect alignment at entry. ema3 not available; ema5 used as documented substitution.
No volume dependency.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "triple_ema_crossover_3_13_144",
    "cadences": ["day"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5 (proxy ema3), ema13, ema144",
    "long": "close > ema144 AND close > ema13 AND ema5 crosses above ema13",
    "short": "close < ema144 AND close < ema13 AND ema5 crosses below ema13",
    "desc": "Triple EMA 3-13-144 crossover (ema3 approximated by ema5)",
    "source": "web:https://www.strategy-workspaceegiesresources.com/trend-following-forex-strategies/70-3ema-s/",
}


def signal(ind, pos, htf=None):
    """Fast EMA crosses medium EMA in direction of slow EMA."""
    c = ind["close"][pos]
    e5, e5p = ind["ema5"][pos], ind["ema5"][pos - 1]
    e13, e13p = ind["ema13"][pos], ind["ema13"][pos - 1]
    e144 = ind["ema144"][pos]
    if nan(c, e5, e5p, e13, e13p, e144):
        return None
    if c > e144 and c > e13 and _xup(e5, e5p, e13, e13p):
        return "long"
    if c < e144 and c < e13 and _xdn(e5, e5p, e13, e13p):
        return "short"
    return None
