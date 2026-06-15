#!/usr/bin/env python3
"""rsi_stochastic_ma_combined -- SMA200 direction + RSI2 extreme + Stoch K OB/OS. cat7 EA (MQL4 2015).

Three-layer: sma200 direction, rsi2 extreme (<20/>80, proxy for RSI3), stoch_k confirmation.
sma200 is the closest available substitute for the source's MA(150).
rsi2 is the closest available substitute for RSI(3).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_stochastic_ma_combined",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "sma200, rsi2, stoch_k, close",
    "long": "close > sma200 AND rsi2 < 20 AND stoch_k < 30",
    "short": "close < sma200 AND rsi2 > 80 AND stoch_k > 70",
    "desc": "Triple-confirm mean-reversion: MA200 trend + RSI2 extreme + Stoch K OB/OS",
    "source": "web:https://www.mql5.com/en/code/13960",
}


def signal(ind, pos, htf=None):
    """SMA200 trend filter + RSI2 extreme + Stochastic K confirmation."""
    c = ind["close"][pos]
    sma = ind["sma200"][pos]
    r2 = ind["rsi2"][pos]
    sk = ind["stoch_k"][pos]
    if nan(c, sma, r2, sk):
        return None
    if c > sma and r2 < 20 and sk < 30:
        return "long"
    if c < sma and r2 > 80 and sk > 70:
        return "short"
    return None
