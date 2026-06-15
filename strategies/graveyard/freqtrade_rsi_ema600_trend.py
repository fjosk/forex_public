#!/usr/bin/env python3
"""freqtrade_rsi_ema600_trend -- RSI cross-above-25 with slow EMA200 regime gate (ema200 proxies ema600). paulcpk."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "freqtrade_rsi_ema600_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h",
    "indicators": "rsi, ema200, low",
    "long": "RSI crosses above 25 AND candle low > EMA200 (slow trend gate; ema200 proxies ema600)",
    "short": "Not used (long-only per source)",
    "desc": "RSI directional with slow EMA trend: RSI cross above 25 in EMA200 uptrend",
    "source": "paulcpk/freqtrade-strategies-that-work RSIDirectionalWithTrendSlow.py",
}


def signal(ind, pos, htf=None):
    """RSI(14) crosses above 25 while candle low is above EMA200 (slow trend confirmation)."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    lo = ind["low"][pos]
    e200 = ind["ema200"][pos]
    if nan(r, r1, lo, e200):
        return None
    # RSI crossover above 25 (momentum turning up from oversold region)
    if r > 25 and r1 <= 25 and lo > e200:
        return "long"
    return None
