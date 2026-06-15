#!/usr/bin/env python3
"""cci_zero_line_cross -- CCI zero-line cross with SMA200 trend filter. PicturePerfect."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "cci_zero_line_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h/4h/daily",
    "indicators": "cci, sma200, close",
    "long": "CCI crosses above 0 from below AND close above sma200",
    "short": "CCI crosses below 0 from above AND close below sma200",
    "desc": "CCI zero-line cross momentum entry with SMA200 trend filter",
    "source": "web:https://pictureperfectportfolios.com/how-to-use-the-commodity-channel-index-cci-in-trading/",
}


def signal(ind, pos, htf=None):
    """CCI zero-cross in trend direction: bullish when CCI flips positive above SMA200."""
    if pos < 1:
        return None
    cci0 = ind["cci"][pos]
    cci1 = ind["cci"][pos - 1]
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    if nan(cci0, cci1, c, s200):
        return None

    if cci0 > 0 and cci1 <= 0 and c > s200:
        return "long"
    if cci0 < 0 and cci1 >= 0 and c < s200:
        return "short"

    return None
