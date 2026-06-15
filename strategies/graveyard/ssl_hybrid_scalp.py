#!/usr/bin/env python3
"""ssl_hybrid_scalp -- SSL Hybrid channel flip scalp. LiteFinance scalping guide.

Enters when ssl_hlv flips from negative to positive (long) or positive to negative (short).
Simple momentum-flip entry; exits on the next opposite flip.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ssl_hybrid_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m-15m",
    "indicators": "ssl_hlv, macd_hist",
    "long": "ssl_hlv flips from <= 0 to > 0 (bullish direction change)",
    "short": "ssl_hlv flips from >= 0 to < 0 (bearish direction change)",
    "desc": "SSL Hybrid channel flip scalp",
    "source": "web:https://www.litefinance.org/blog/for-beginners/trading-strategies/scalping-forex/",
}


def signal(ind, pos, htf=None):
    """SSL Hybrid channel flip scalp."""
    s0 = ind["ssl_hlv"][pos]
    s1 = ind["ssl_hlv"][pos - 1]
    if nan(s0, s1):
        return None
    if s0 > 0 and s1 <= 0:
        return "long"
    if s0 < 0 and s1 >= 0:
        return "short"
    return None
