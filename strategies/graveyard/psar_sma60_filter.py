#!/usr/bin/env python3
"""psar_sma60_filter -- PSAR flip confirmed by price vs SMA50 (proxy for SMA60). mql5 article 15698."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "psar_sma60_filter",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "psar, psar_dir, sma50, low, high, close",
    "long": "PSAR flips bullish (psar_dir[pos-1]<0 -> psar_dir[pos]>0) AND close > sma50",
    "short": "PSAR flips bearish (psar_dir[pos-1]>0 -> psar_dir[pos]<0) AND close < sma50",
    "desc": "PSAR flip with SMA50 trend filter (SMA60 approximated by SMA50)",
    "source": "mql5.com article 15698 -- Rapid-Fire SAR-SMA EA (2024); SMA60->SMA50 approximation",
}


def signal(ind, pos, htf=None):
    """PSAR directional flip gated by price position relative to SMA50."""
    d = ind["psar_dir"][pos]
    d1 = ind["psar_dir"][pos - 1]
    s50 = ind["sma50"][pos]
    c = ind["close"][pos]
    if nan(d, d1, s50, c):
        return None
    flip_bull = d1 < 0 and d > 0
    flip_bear = d1 > 0 and d < 0
    if flip_bull and c > s50:
        return "long"
    if flip_bear and c < s50:
        return "short"
    return None
