#!/usr/bin/env python3
"""rsi_ob_os_pullback -- RSI extreme exit in trend direction (EMA200 filter). EarnForex."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_ob_os_pullback",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h/4h",
    "indicators": "ema200, rsi",
    "long": "close above ema200 AND RSI crosses back above 30 (exits oversold)",
    "short": "close below ema200 AND RSI crosses back below 70 (exits overbought)",
    "desc": "RSI overbought/oversold pullback entry in EMA200 trend direction",
    "source": "web:https://www.earnforex.com/guides/trading-strategies/",
}


def signal(ind, pos, htf=None):
    """In-trend RSI extreme exit: buy dip when RSI exits oversold in uptrend."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    r0 = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    if nan(c, e200, r0, r1):
        return None

    if c > e200 and r0 > 30 and r1 <= 30:
        return "long"
    if c < e200 and r0 < 70 and r1 >= 70:
        return "short"

    return None
