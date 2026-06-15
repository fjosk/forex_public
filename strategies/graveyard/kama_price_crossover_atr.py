#!/usr/bin/env python3
"""kama_price_crossover_atr -- KAMA price crossover with ATR volatility filter. web:https://datadave1.medium.com/kaufman-adaptive-moving-average-and-atr-long-position-strategy-416714e07c19"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "kama_price_crossover_atr",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "kama, atr_pct, close",
    "long": "KAMA rising AND atr_pct > 0.3% AND close crosses above KAMA",
    "short": "KAMA falling AND atr_pct > 0.3% AND close crosses below KAMA",
    "desc": "KAMA crossover with ATR volatility floor filter to avoid flat-market whipsaws",
    "source": "web:https://datadave1.medium.com/kaufman-adaptive-moving-average-and-atr-long-position-strategy-416714e07c19",
}


def signal(ind, pos, htf=None):
    """Price crosses KAMA in direction of KAMA slope with minimum volatility."""
    kama = ind["kama"][pos]
    kama1 = ind["kama"][pos - 1]
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    atr_pct = ind["atr_pct"][pos]
    if nan(kama, kama1, c, c1, atr_pct):
        return None
    kama_rising = kama > kama1
    kama_falling = kama < kama1
    vol_ok = atr_pct > 0.003
    cross_above = c > kama and c1 <= kama1
    cross_below = c < kama and c1 >= kama1
    if kama_rising and vol_ok and cross_above:
        return "long"
    if kama_falling and vol_ok and cross_below:
        return "short"
    return None
