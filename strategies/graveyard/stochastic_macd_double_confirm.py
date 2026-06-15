#!/usr/bin/env python3
"""stochastic_macd_double_confirm -- Stochastic K+D both extreme + MACD histogram sign. Nikhil-Adithyan.

Long when stoch_k < 30 AND stoch_d < 30 AND macd_hist < 0 (bearish momentum, mean-reversion long).
Short when stoch_k > 70 AND stoch_d > 70 AND macd_hist > 0.
The source uses fixed MACD value thresholds (< -2 / > 2); replaced with macd_hist sign for FX
compatibility (FX MACD values are pip-scale, not equity-scale).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_macd_double_confirm",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1d",
    "indicators": "stoch_k, stoch_d, macd_hist",
    "long": "stoch_k < 30 AND stoch_d < 30 AND macd_hist < 0 (all deeply bearish -> mean-rev long)",
    "short": "stoch_k > 70 AND stoch_d > 70 AND macd_hist > 0 (all deeply bullish -> mean-rev short)",
    "desc": "Double oscillator extreme + MACD histogram sign; Stoch+MACD four-condition confirmation",
    "source": "web:https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python",
}


def signal(ind, pos, htf=None):
    """Stochastic K+D both extreme + MACD histogram confirms bearish/bullish momentum."""
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    mh = ind["macd_hist"][pos]
    if nan(sk, sd, mh):
        return None
    if sk < 30 and sd < 30 and mh < 0:
        return "long"
    if sk > 70 and sd > 70 and mh > 0:
        return "short"
    return None
