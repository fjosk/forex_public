#!/usr/bin/env python3
"""sma_crossover_pullback -- SMA100/200 golden/death cross + stochastic pullback entry. BabyPips."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "sma_crossover_pullback",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "sma100, sma200, stoch_k",
    "long": "sma100 > sma200 (golden cross state) AND stoch_k crosses above 25 (pullback confirmed)",
    "short": "sma100 < sma200 (death cross state) AND stoch_k crosses below 75",
    "desc": "SMA100/200 trend state + stochastic pullback from extreme zone as entry trigger",
    "source": "web:https://www.babypips.com/trading/forex-system-20150605",
}


def signal(ind, pos, htf=None):
    """SMA100/200 trend state + stochastic pullback trigger."""
    s100 = ind["sma100"][pos]
    s200 = ind["sma200"][pos]
    sk = ind["stoch_k"][pos]
    skp = ind["stoch_k"][pos - 1]
    if nan(s100, s200, sk, skp):
        return None
    trend_long = s100 > s200
    trend_short = s100 < s200
    # Pullback: stoch crosses back out of extreme zone
    stoch_up = sk > 25 and skp <= 25
    stoch_dn = sk < 75 and skp >= 75
    if trend_long and stoch_up:
        return "long"
    if trend_short and stoch_dn:
        return "short"
    return None
