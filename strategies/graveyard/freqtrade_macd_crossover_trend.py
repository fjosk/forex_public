#!/usr/bin/env python3
"""freqtrade_macd_crossover_trend -- Freqtrade MACD Zero-Cross with EMA Trend Guard. paulcpk.

MACD < 0 AND macd_sig crosses above macd AND low > ema50 (ema100 proxied by ema50).
Long-only in source. Symmetric short added for FX.
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "freqtrade_macd_crossover_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "macd, macd_sig, ema50, low, high",
    "long": "macd < 0 AND macd_sig crosses above macd (signal above line) AND low > ema50",
    "short": "macd > 0 AND macd crosses above macd_sig from below AND high < ema50",
    "desc": "MACD below-zero crossover with EMA50 trend guard (EMA100 proxy)",
    "source": "web:https://github.com/paulcpk/freqtrade-strategies-that-work/blob/master/MACDCrossoverWithTrend.py",
}


def signal(ind, pos, htf=None):
    """MACD below-zero crossover gated by EMA50 trend filter."""
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    ms = ind["macd_sig"][pos]
    ms1 = ind["macd_sig"][pos - 1]
    e50 = ind["ema50"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    if nan(m, m1, ms, ms1, e50, lo, hi):
        return None
    # Long: signal crosses above macd line while macd < 0, candle low above ema50
    if m < 0 and _xup(ms, ms1, m, m1) and lo > e50:
        return "long"
    # Short: macd crosses above signal while macd > 0, candle high below ema50
    if m > 0 and _xup(m, m1, ms, ms1) and hi < e50:
        return "short"
    return None
