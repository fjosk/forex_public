#!/usr/bin/env python3
"""adx_ema14_trend_scalp -- ADX(14) > 25 trend filter + EMA13 candle close. web:forextester.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_ema14_trend_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "15m",
    "indicators": "adx, ema13 (proxy ema14)",
    "long": "ADX > 25 AND bullish candle closes above EMA13",
    "short": "ADX > 25 AND bearish candle closes below EMA13",
    "desc": "ADX(14) > 25 trend filter + EMA13 candle close scalp",
    "source": "web:https://forextester.com/blog/adx-14-ema-strategy/",
}


def signal(ind, pos, htf=None):
    """ADX trend-strong filter with EMA13 candle-close entry."""
    adx = ind["adx"][pos]
    ema = ind["ema13"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    if nan(adx, ema, c, o):
        return None
    trend_strong = adx > 25
    if not trend_strong:
        return None
    if c > ema and c > o:
        return "long"
    if c < ema and c < o:
        return "short"
    return None
