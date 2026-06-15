#!/usr/bin/env python3
"""williams_pct_r_ema_filter -- Williams %R midline cross filtered by EMA200 trend. mql5 articles/11142.

Williams %R crosses above/below -50 midline only in the EMA200 trend direction (System 3).
EMA100 from spec approximated by EMA200 (closest available key).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "williams_pct_r_ema_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "willr, ema200",
    "long": "close > EMA200 AND Williams %R > -50 (momentum bullish in uptrend)",
    "short": "close < EMA200 AND Williams %R < -50 (momentum bearish in downtrend)",
    "desc": "Williams %R -50 midline with EMA200 trend filter (System 3)",
    "source": "https://www.mql5.com/en/articles/11142 Williams %R System 3",
}


def signal(ind, pos, htf=None):
    """Williams %R -50 cross in EMA200 trend direction."""
    w = ind["willr"][pos]
    w1 = ind["willr"][pos - 1]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(w, w1, c, e200):
        return None
    if c > e200 and w > -50 and w1 <= -50:
        return "long"
    if c < e200 and w < -50 and w1 >= -50:
        return "short"
    return None
