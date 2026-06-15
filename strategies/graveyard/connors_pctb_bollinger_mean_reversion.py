#!/usr/bin/env python3
"""connors_pctb_bollinger_mean_reversion -- Connors Percent-B Bollinger mean reversion. Larry Connors / QuantifiedStrategies.

Bollinger %B below 0.2 for three consecutive bars while price > SMA200 -> long.
%B above 0.8 for three consecutive bars while price < SMA200 -> short.
Source: web:https://www.quantifiedstrategies.com/larry-connors-b-strategy-bollinger-band/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "connors_pctb_bollinger_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "bb_pctb, sma200, bb_mid, close",
    "long": "close > sma200; bb_pctb < 0.2 for 3 consecutive bars (extreme lower-band hug)",
    "short": "close < sma200; bb_pctb > 0.8 for 3 consecutive bars (extreme upper-band hug)",
    "desc": "Connors %B: three-consecutive-bar extreme below/above BB bands in trend direction",
    "source": "web:https://www.quantifiedstrategies.com/larry-connors-b-strategy-bollinger-band/",
}


def signal(ind, pos, htf=None):
    """Connors %B: three consecutive extreme %B readings with SMA200 trend filter."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    bp0 = ind["bb_pctb"][pos]
    bp1 = ind["bb_pctb"][pos - 1]
    bp2 = ind["bb_pctb"][pos - 2]
    if nan(c, s200, bp0, bp1, bp2):
        return None

    if c > s200 and bp0 < 0.2 and bp1 < 0.2 and bp2 < 0.2:
        return "long"
    if c < s200 and bp0 > 0.8 and bp1 > 0.8 and bp2 > 0.8:
        return "short"

    return None
