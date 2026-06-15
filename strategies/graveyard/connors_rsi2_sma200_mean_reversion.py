#!/usr/bin/env python3
"""connors_rsi2_sma200_mean_reversion -- Connors RSI-2 Mean Reversion with SMA200 Trend Filter."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "connors_rsi2_sma200_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "rsi2, sma200, close_sma5",
    "long": "close > sma200 AND rsi2 < 5 (extreme oversold in uptrend)",
    "short": "close < sma200 AND rsi2 > 95 (extreme overbought in downtrend)",
    "desc": "Larry Connors RSI(2) mean reversion with SMA200 bull/bear regime filter",
    "source": "medium.com/@FMZQuant/larry-connors-rsi2-mean-reversion-strategy; Connors & Alvarez 2008",
}


def signal(ind, pos, htf=None):
    """Connors RSI(2) mean reversion gated by SMA200 regime."""
    c = ind["close"][pos]
    r2 = ind["rsi2"][pos]
    s200 = ind["sma200"][pos]
    if nan(c, r2, s200):
        return None
    if c > s200 and r2 < 5:
        return "long"
    if c < s200 and r2 > 95:
        return "short"
    return None
