#!/usr/bin/env python3
"""paperswithbacktest_pu_mean_reversion -- OU single-instrument mean reversion: hurst-gated z-score via ema200+atr.

Approximates the OU z-score as (close - ema200) / atr, gated by hurst < 0.45 (mean-reverting regime).
Thresholds at +/-1.5 sigma equivalent. No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "paperswithbacktest_pu_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1d",
    "indicators": "ema200, atr, close, hurst",
    "long": "hurst < 0.45 AND z-score < -1.5 (z = (close-ema200)/atr*sqrt2)",
    "short": "hurst < 0.45 AND z-score > +1.5",
    "desc": "PwB OU mean reversion: Hurst-gated ATR-scaled z-score vs EMA200 long-run mean",
    "source": "paperswithbacktest.com systematic-trading OU toolbox; Dixit & Pindyck 1994",
}

import math

_Z_ENTRY = 1.5
_SQRT2 = math.sqrt(2.0)


def signal(ind, pos, htf=None):
    """Hurst-gated OU z-score mean reversion."""
    h = ind["hurst"][pos]
    e200 = ind["ema200"][pos]
    at = ind["atr"][pos]
    cl = ind["close"][pos]
    if nan(h, e200, at, cl):
        return None
    # Only trade when market is in mean-reverting regime
    if h >= 0.45:
        return None
    if at <= 0:
        return None
    # OU sigma approximation: sigma / sqrt(2*theta) ~ atr * sqrt(2)
    sigma_approx = at * _SQRT2
    z = (cl - e200) / sigma_approx
    if z < -_Z_ENTRY:
        return "long"
    if z > _Z_ENTRY:
        return "short"
    return None
