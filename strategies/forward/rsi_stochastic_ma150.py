#!/usr/bin/env python3
"""rsi_stochastic_ma150 -- MA200 trend + RSI extreme + Stoch K pullback. barabashkakvn MQL5 2017.

Trade mean-reversion pullbacks in direction of SMA200 trend.
Uses sma200 as proxy for MA(150); rsi (14) as proxy for RSI(3) with adjusted thresholds.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_stochastic_ma150",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h",
    "indicators": "sma200, rsi, stoch_k, close",
    "long": "close > sma200 AND rsi < 30 AND stoch_k < 30",
    "short": "close < sma200 AND rsi > 70 AND stoch_k > 70",
    "desc": "SMA200 trend + RSI + Stochastic pullback mean-reversion; proxy for MA150/RSI3 original",
    "source": "web:https://www.mql5.com/en/code/18671",
}


def signal(ind, pos, htf=None):
    """SMA200 direction filter + RSI oversold/overbought + Stochastic K confirmation."""
    c = ind["close"][pos]
    sma = ind["sma200"][pos]
    r = ind["rsi"][pos]
    sk = ind["stoch_k"][pos]
    if nan(c, sma, r, sk):
        return None
    if c > sma and r < 30 and sk < 30:
        return "long"
    if c < sma and r > 70 and sk > 70:
        return "short"
    return None
