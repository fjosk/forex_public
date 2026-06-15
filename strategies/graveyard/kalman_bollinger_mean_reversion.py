#!/usr/bin/env python3
"""kalman_bollinger_mean_reversion -- Kalman Filter + BB Mean-Reversion (KF degraded to standard BB)."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "kalman_bollinger_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_pctb, bb_lo, bb_up",
    "long": "bb_pctb < 0 (close below lower band -- equivalent to KF band breach)",
    "short": "bb_pctb > 1 (close above upper band)",
    "desc": "Kalman BB mean reversion degraded to standard BB (KF parameter tuning not pre-computed)",
    "source": "github.com/marcoscobo/AlgorithmicTradingKF",
}


def signal(ind, pos, htf=None):
    """Standard BB band breach as KF-BB proxy; bb_pctb outside [0,1] = beyond the bands."""
    pctb = ind["bb_pctb"][pos]
    if nan(pctb):
        return None
    if pctb < 0:
        return "long"
    if pctb > 1:
        return "short"
    return None
