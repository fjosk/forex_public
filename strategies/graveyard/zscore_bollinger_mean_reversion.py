#!/usr/bin/env python3
"""zscore_bollinger_mean_reversion -- Bollinger %B below 0 / above 1 with ADX<25 regime filter.

Long when bb_pctb < 0 (price below lower band, z-score < -2) in a low-trend regime (ADX < 25).
Short when bb_pctb > 1 (above upper band). Target: reversion to bb_mid.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "zscore_bollinger_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "bb_pctb, adx",
    "long": "bb_pctb < 0 (below lower BB) and ADX < 25 (range-bound regime)",
    "short": "bb_pctb > 1 (above upper BB) and ADX < 25",
    "desc": "Bollinger Band z-score extreme mean reversion with ADX range filter",
    "source": "web:https://medium.com/@kridtapon/trading-mean-reversion-with-z-score-a-simple-yet-powerful-strategy-173fdfb3fbc2",
}


def signal(ind, pos, htf=None):
    """BB extreme fade in range regime."""
    bp = ind["bb_pctb"][pos]
    adx_v = ind["adx"][pos]
    if nan(bp, adx_v):
        return None
    if adx_v >= 25:
        return None  # trending regime, skip reversion
    if bp < 0.0:
        return "long"
    if bp > 1.0:
        return "short"
    return None
