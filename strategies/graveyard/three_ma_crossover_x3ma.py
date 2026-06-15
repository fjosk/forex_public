#!/usr/bin/env python3
"""three_ma_crossover_x3ma -- Three-MA cascade alignment entry. X3MA EA (m-root MQL4)."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "three_ma_crossover_x3ma",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5, ema21, ema50",
    "long": "ema5 > ema21 > ema50 (full bull stack) AND ema5[pos-1] <= ema21[pos-1] (fresh cross)",
    "short": "ema5 < ema21 < ema50 (full bear stack) AND ema5[pos-1] >= ema21[pos-1] (fresh cross)",
    "desc": "Three-MA alignment (ema5/21/50): enter when fastest MA crosses medium and all three stack",
    "source": "X3MA EA by m-root (github.com/m-root/THREE-MOVING-AVERAGE-Expert-Advisor, MQL4)",
}


def signal(ind, pos, htf=None):
    """All three EMAs must stack in the direction; entry triggered by ema5 crossing ema21."""
    f = ind["ema5"][pos]
    m = ind["ema21"][pos]
    s = ind["ema50"][pos]
    f1 = ind["ema5"][pos - 1]
    m1 = ind["ema21"][pos - 1]
    if nan(f, m, s, f1, m1):
        return None
    if f > m > s and f1 <= m1:
        return "long"
    if f < m < s and f1 >= m1:
        return "short"
    return None
