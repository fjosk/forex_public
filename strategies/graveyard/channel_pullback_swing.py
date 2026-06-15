#!/usr/bin/env python3
"""channel_pullback_swing -- Channel Pullback Mean-Reversion Swing. Stocks & Commodities Dec 2016."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "channel_pullback_swing",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "hh_n, ll_n, sma50",
    "long": "price recovers through midchannel from below AND close > sma50",
    "short": "price breaks through midchannel from above AND close < sma50",
    "desc": "20-bar channel midpoint re-cross with SMA50 trend filter (Stocks & Commodities 2016)",
    "source": "gist.github.com/sherwind/405acc2706d5416865bc0e33941189d9",
}


def signal(ind, pos, htf=None):
    """Price crosses 20-bar channel midpoint with SMA50 trend filter."""
    hh = ind["hh_n"][pos]
    ll = ind["ll_n"][pos]
    s50 = ind["sma50"][pos]
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    if nan(hh, ll, s50, c, c1):
        return None
    mid = (hh + ll) / 2.0
    if c > mid and c1 <= mid and c > s50:
        return "long"
    if c < mid and c1 >= mid and c < s50:
        return "short"
    return None
