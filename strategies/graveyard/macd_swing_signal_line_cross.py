#!/usr/bin/env python3
"""macd_swing_signal_line_cross -- MACD histogram sign-change with SMA200 filter. QuantifiedStrategies."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_swing_signal_line_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "daily",
    "indicators": "macd_hist, sma200, close",
    "long": "MACD histogram crosses from negative to positive AND close above sma200",
    "short": "MACD histogram crosses from positive to negative AND close below sma200",
    "desc": "MACD swing signal-line cross: histogram zero-cross with SMA200 trend filter",
    "source": "web:https://www.quantifiedstrategies.com/macd-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """MACD histogram sign-change in SMA200 trend direction."""
    if pos < 1:
        return None
    mh0 = ind["macd_hist"][pos]
    mh1 = ind["macd_hist"][pos - 1]
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    if nan(mh0, mh1, c, s200):
        return None

    if mh0 >= 0 and mh1 < 0 and c > s200:
        return "long"
    if mh0 < 0 and mh1 >= 0 and c < s200:
        return "short"

    return None
