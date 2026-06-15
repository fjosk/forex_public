#!/usr/bin/env python3
"""sar_stochastic_trend -- PSAR direction with stochastic K-D cross confirmation. armelf/Financial-Algorithms.

PSAR gives directional bias; stochastic K-D spread confirms the entry timing.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "sar_stochastic_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "psar_dir, stoch_k, stoch_d",
    "long": "PSAR below price AND stoch_k > stoch_d (K-D cross positive)",
    "short": "PSAR above price AND stoch_k < stoch_d (K-D cross negative)",
    "desc": "SAR trend direction with stochastic K-D timing confirmation",
    "source": "https://github.com/armelf/Financial-Algorithms SAR Stochastic strategy",
}


def signal(ind, pos, htf=None):
    """PSAR direction with stochastic K-D confirmation."""
    d = ind["psar_dir"][pos]
    k = ind["stoch_k"][pos]
    k1 = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sd1 = ind["stoch_d"][pos - 1]
    if nan(d, k, k1, sd, sd1):
        return None
    kd = k - sd
    kd1 = k1 - sd1
    if d == 1 and kd > 0 and kd1 <= 0:
        return "long"
    if d == -1 and kd < 0 and kd1 >= 0:
        return "short"
    return None
