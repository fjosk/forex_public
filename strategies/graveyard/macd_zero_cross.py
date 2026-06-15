#!/usr/bin/env python3
"""macd_zero_cross -- MACD line crosses zero with SMA200 trend filter. DailyFX."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_zero_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h/daily",
    "indicators": "macd, sma200, close",
    "long": "MACD line crosses above zero AND close above sma200",
    "short": "MACD line crosses below zero AND close below sma200",
    "desc": "MACD zero-line cross momentum entry with SMA200 trend confirmation",
    "source": "web:https://www.dailyfx.com/education/moving-average-convergence-divergence/macd-trading-strategy.html",
}


def signal(ind, pos, htf=None):
    """MACD crosses zero in SMA200 trend direction."""
    if pos < 1:
        return None
    m0 = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    if nan(m0, m1, c, s200):
        return None

    if m0 > 0 and m1 <= 0 and c > s200:
        return "long"
    if m0 < 0 and m1 >= 0 and c < s200:
        return "short"

    return None
