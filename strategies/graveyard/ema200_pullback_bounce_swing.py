#!/usr/bin/env python3
"""ema200_pullback_bounce_swing -- EMA200 dynamic support/resistance bounce. web:https://blog.opofinance.com/en/200-ema-swing-trading/"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema200_pullback_bounce_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema200, atr, close, open",
    "long": "close above ema200, price near ema200 (within 0.5 ATR), bullish candle",
    "short": "close below ema200, price near ema200, bearish candle",
    "desc": "EMA200 pullback bounce swing -- enter the bounce at the dynamic MA",
    "source": "web:https://blog.opofinance.com/en/200-ema-swing-trading/",
}


def signal(ind, pos, htf=None):
    """EMA200 proximity bounce with candle direction confirmation."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    e200 = ind["ema200"][pos]
    atr = ind["atr"][pos]
    if nan(c, o, e200, atr):
        return None
    trend_up = c > e200
    trend_dn = c < e200
    near_ema = abs(c - e200) < atr * 0.5
    bull_bar = c > o
    bear_bar = c < o
    if trend_up and near_ema and bull_bar:
        return "long"
    if trend_dn and near_ema and bear_bar:
        return "short"
    return None
