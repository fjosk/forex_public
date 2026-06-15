#!/usr/bin/env python3
"""raschke_first_cross_pullback_trend_entry -- Raschke First Cross: oscillator (MACD) pulls back to signal line after momentum burst; low holding = long entry. Kaufman.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "raschke_first_cross_pullback_trend_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "macd, macd_sig, high, low",
    "long": "MACD was above signal, now crosses back to/below signal AND low > prior low (pullback holding)",
    "short": "MACD was below signal, crosses back to/above signal AND high < prior high (pullback holding)",
    "desc": "Raschke First Cross: first pullback-to-signal-line after a momentum burst with price holding structure",
    "source": "Kaufman, Trading Systems and Methods, Applications of Single Trends - Raschke's First Cross",
}


def signal(ind, pos, htf=None):
    """First oscillator pullback to signal line while price structure holds."""
    if pos < 1:
        return None
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    s = ind["macd_sig"][pos]
    s1 = ind["macd_sig"][pos - 1]
    lo = ind["low"][pos]
    lo1 = ind["low"][pos - 1]
    hi = ind["high"][pos]
    hi1 = ind["high"][pos - 1]
    if nan(m, m1, s, s1, lo, lo1, hi, hi1):
        return None
    # Long: prior bar osc above signal, current crosses at/below signal AND low holding
    if m1 > s1 and m <= s and lo > lo1:
        return "long"
    # Short: prior bar osc below signal, current crosses at/above signal AND high holding
    if m1 < s1 and m >= s and hi < hi1:
        return "short"
    return None
