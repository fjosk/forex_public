#!/usr/bin/env python3
"""rsi_sma200_dual_threshold -- RSI 30/70 mean reversion gated by SMA200 trend filter. FMZQuant/Connors."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_sma200_dual_threshold",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "rsi, sma200, close",
    "long": "RSI < 30 (oversold) AND close > sma200 (uptrend)",
    "short": "RSI > 70 (overbought) AND close < sma200 (downtrend)",
    "desc": "RSI dual-threshold mean reversion with SMA200 trend gate",
    "source": "FMZQuant/Larry Connors RSI mean reversion (medium.com/@FMZQuant); DataCamp Python implementation",
}


def signal(ind, pos, htf=None):
    """Buy oversold dips in uptrend; sell overbought spikes in downtrend."""
    r = ind["rsi"][pos]
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    if nan(r, c, s200):
        return None
    if r < 30 and c > s200:
        return "long"
    if r > 70 and c < s200:
        return "short"
    return None
