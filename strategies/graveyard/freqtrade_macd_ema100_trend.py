#!/usr/bin/env python3
"""freqtrade_macd_ema100_trend -- MACD signal crosses MACD below zero + price above EMA100 proxy. paulcpk."""
from strategies._common import nan, TREND, _xup, ALL_CLASSES

# EMA100 is not available; ema50 is used as a proxy (the closest available key < 200).

META = {
    "id": "freqtrade_macd_ema100_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "macd, macd_sig, ema50, low",
    "long": "macd < 0 AND macd_sig crosses above macd AND low > ema50 (ema100 proxy)",
    "short": "not used (long-only per source)",
    "desc": "MACD bullish crossover below zero with EMA50 trend filter (EMA100 proxy)",
    "source": "https://github.com/paulcpk/freqtrade-strategies-that-work/blob/master/MACDCrossoverWithTrend.py",
}


def signal(ind, pos, htf=None):
    """MACD signal x MACD below zero + EMA50 trend filter."""
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    ms1 = ind["macd_sig"][pos - 1]
    m1 = ind["macd"][pos - 1]
    e50 = ind["ema50"][pos]
    lo = ind["low"][pos]
    if nan(m, ms, ms1, m1, e50, lo):
        return None
    # Long: MACD below zero with signal crossing above MACD line, price in uptrend
    if m < 0 and _xup(ms, ms1, m, m1) and lo > e50:
        return "long"
    return None
