#!/usr/bin/env python3
"""cci_ema34_5m -- CCI(20) crosses +/-90 with price on correct side of EMA50. web:tradersunion.com."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "cci_ema34_5m",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "cci, ema50 (proxy ema34)",
    "long": "close > ema50 AND CCI crosses above +90",
    "short": "close < ema50 AND CCI crosses below -90",
    "desc": "CCI(20) breakout of +/-90 level with EMA50 trend filter scalp",
    "source": "web:https://tradersunion.com/interesting-articles/trading-strategies/scalping-strategies/",
}


def signal(ind, pos, htf=None):
    """CCI crosses the +90 or -90 extreme while price is on the right side of EMA50."""
    cci = ind["cci"][pos]
    cci_p = ind["cci"][pos - 1]
    ema = ind["ema50"][pos]
    c = ind["close"][pos]
    if nan(cci, cci_p, ema, c):
        return None
    if c > ema and _xup(cci, cci_p, 90, 90):
        return "long"
    if c < ema and _xdn(cci, cci_p, -90, -90):
        return "short"
    return None
