#!/usr/bin/env python3
"""hurst_exponent_regime_filter -- Hurst exponent regime gate + SMA20/SMA50 trend or RSI mean-rev.

H > 0.55: trending regime -> SMA20 > SMA50 = long, SMA20 < SMA50 = short.
H < 0.45: mean-reverting regime -> RSI < 30 = long, RSI > 70 = short.
0.45 <= H <= 0.55: random walk -> no entry.
"""
from strategies._common import nan, TREND, REVERT, ALL_CLASSES

META = {
    "id": "hurst_exponent_regime_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "hurst, sma20, sma50, rsi",
    "long": "H > 0.55: sma20 > sma50; H < 0.45: rsi < 30",
    "short": "H > 0.55: sma20 < sma50; H < 0.45: rsi > 70",
    "desc": "Hurst regime classifier gates trend-following vs mean-reversion entry",
    "source": "web:https://github.com/Sidhus234/Hurst-Exponent-Trading-Strategy",
}


def signal(ind, pos, htf=None):
    """Hurst exponent selects regime; applies appropriate entry rule."""
    h = ind["hurst"][pos]
    s20 = ind["sma20"][pos]
    s50 = ind["sma50"][pos]
    r = ind["rsi"][pos]
    if nan(h, s20, s50, r):
        return None
    if h > 0.55:
        # Trending regime: SMA cross direction
        if s20 > s50:
            return "long"
        if s20 < s50:
            return "short"
    elif h < 0.45:
        # Mean-reverting regime: RSI OB/OS
        if r < 30:
            return "long"
        if r > 70:
            return "short"
    return None
