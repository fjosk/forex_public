#!/usr/bin/env python3
"""macd_histogram_zero_cross -- MACD histogram sign-change with EMA200 trend filter. QuantifiedStrategies."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_histogram_zero_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h/4h/daily",
    "indicators": "macd_hist, ema200, close",
    "long": "MACD histogram crosses above 0 AND close above ema200",
    "short": "MACD histogram crosses below 0 AND close below ema200",
    "desc": "MACD histogram zero-cross momentum entry with EMA200 trend filter",
    "source": "web:https://www.quantifiedstrategies.com/macd-histogram/",
}


def signal(ind, pos, htf=None):
    """MACD histogram sign-change in trend direction."""
    if pos < 1:
        return None
    mh0 = ind["macd_hist"][pos]
    mh1 = ind["macd_hist"][pos - 1]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(mh0, mh1, c, e200):
        return None

    if mh0 > 0 and mh1 <= 0 and c > e200:
        return "long"
    if mh0 < 0 and mh1 >= 0 and c < e200:
        return "short"

    return None
