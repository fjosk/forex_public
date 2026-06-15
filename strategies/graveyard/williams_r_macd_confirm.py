#!/usr/bin/env python3
"""williams_r_macd_confirm -- Williams %R -50 crossover with MACD confirmation. Nikhil-Adithyan.

Williams %R crosses the -50 midline while MACD confirms the direction.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "williams_r_macd_confirm",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "willr, macd, macd_sig",
    "long": "Williams %R crosses below -50 (downward entry) AND MACD > macd_sig",
    "short": "Williams %R crosses above -50 (upward exit zone) AND MACD < macd_sig",
    "desc": "Williams %R -50 midline cross with MACD direction confirmation",
    "source": "https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python Williams%R_MACD.py",
}


def signal(ind, pos, htf=None):
    """Williams %R -50 cross with MACD confirmation."""
    w = ind["willr"][pos]
    w1 = ind["willr"][pos - 1]
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    if nan(w, w1, m, ms):
        return None
    # Long: WR crosses below -50 (entering oversold pressure) AND MACD bullish
    if w1 > -50 and w < -50 and m > ms:
        return "long"
    # Short: WR crosses above -50 (leaving oversold, overbought territory) AND MACD bearish
    if w1 < -50 and w > -50 and m < ms:
        return "short"
    return None
