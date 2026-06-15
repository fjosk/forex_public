#!/usr/bin/env python3
"""jesse_macd_ema -- MACD above signal AND close above EMA50 (EMA100 proxy). jesse-ai example."""
from strategies._common import nan, TREND, ALL_CLASSES

# EMA100 not available; ema50 used as proxy (closest available).

META = {
    "id": "jesse_macd_ema",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd, macd_sig, ema50, close",
    "long": "macd > macd_sig AND close > ema50 (EMA100 proxy)",
    "short": "macd < macd_sig AND close < ema50 (condition flip of long)",
    "desc": "Jesse MACD + EMA trend filter: macd above signal line and price above EMA50",
    "source": "https://github.com/jesse-ai/example-strategies/blob/master/MACD_EMA/__init__.py",
}


def signal(ind, pos, htf=None):
    """MACD above signal with EMA50 trend filter."""
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    e50 = ind["ema50"][pos]
    c = ind["close"][pos]
    m1 = ind["macd"][pos - 1]
    ms1 = ind["macd_sig"][pos - 1]
    if nan(m, ms, e50, c, m1, ms1):
        return None
    # Long: MACD crosses above signal with price above EMA50
    if m > ms and m1 <= ms1 and c > e50:
        return "long"
    # Short: MACD crosses below signal with price below EMA50
    if m < ms and m1 >= ms1 and c < e50:
        return "short"
    return None
