#!/usr/bin/env python3
"""rsi2_sma200_mean_reversion -- Connors RSI-2 oversold pull-back within SMA200 uptrend. handiko GitHub."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi2_sma200_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "rsi2, sma200, close, high",
    "long": "close > sma200 (uptrend) AND rsi2 < 10 (deeply oversold)",
    "short": "close < sma200 (downtrend) AND rsi2 > 90 (deeply overbought, symmetric FX mirror)",
    "desc": "Connors RSI-2 mean reversion within SMA200 trend filter",
    "source": "handiko/RSI-2-Portfolio-Trading-Strategy-Backtester GitHub; Larry Connors RSI-2 system",
}


def signal(ind, pos, htf=None):
    """RSI(2) deeply oversold pull-back within SMA200-confirmed trend direction."""
    r2 = ind["rsi2"][pos]
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    if nan(r2, c, s200):
        return None
    if c > s200 and r2 < 10:
        return "long"
    if c < s200 and r2 > 90:
        return "short"
    return None
