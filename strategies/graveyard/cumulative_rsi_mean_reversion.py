#!/usr/bin/env python3
"""cumulative_rsi_mean_reversion -- Cumulative RSI(2) mean reversion. Larry Connors / QuantifiedStrategies.

Sum of RSI(2) over three consecutive bars < 20 (sustained oversold) with price > SMA200.
Exit: close above the 5-bar SMA. More selective than single-day RSI(2).
Source: web:https://www.quantifiedstrategies.com/cumulative-rsi-indicator/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "cumulative_rsi_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "rsi2, sma200, close_sma5, close",
    "long": "close > sma200; sum(rsi2[0]+rsi2[-1]+rsi2[-2]) < 20 (sustained oversold 3 bars)",
    "short": "close < sma200; sum(rsi2 x3) > 280 (sustained overbought 3 bars)",
    "desc": "Cumulative RSI(2) 3-bar sum: sustained oversold/overbought filter above/below SMA200",
    "source": "web:https://www.quantifiedstrategies.com/cumulative-rsi-indicator/",
}


def signal(ind, pos, htf=None):
    """cuRSI: 3-day sum of RSI(2) below 20 (long) or above 280 (short) with SMA200 filter."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    r0 = ind["rsi2"][pos]
    r1 = ind["rsi2"][pos - 1]
    r2 = ind["rsi2"][pos - 2]
    if nan(c, s200, r0, r1, r2):
        return None

    cursi = r0 + r1 + r2

    if c > s200 and cursi < 20.0:
        return "long"
    if c < s200 and cursi > 280.0:
        return "short"

    return None
