#!/usr/bin/env python3
"""qqe_swing_daily -- QQE oversold/overbought bounce with EMA200 filter. TheForexGeek."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "qqe_swing_daily",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "daily",
    "indicators": "qqe_line, ema200, close, open",
    "long": "qqe_line < 30 (oversold) AND bullish candle AND close above ema200",
    "short": "qqe_line > 70 (overbought) AND bearish candle AND close below ema200",
    "desc": "QQE oversold/overbought swing with EMA200 trend filter and candle confirmation",
    "source": "web:https://theforexgeek.com/qqe-strategy/",
}


def signal(ind, pos, htf=None):
    """QQE extreme zone bounce: long when oversold with bullish candle in uptrend."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    ql = ind["qqe_line"][pos]
    e200 = ind["ema200"][pos]
    if nan(c, o, ql, e200):
        return None

    if ql < 30 and c > o and c > e200:
        return "long"
    if ql > 70 and c < o and c < e200:
        return "short"

    return None
