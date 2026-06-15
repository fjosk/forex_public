#!/usr/bin/env python3
"""wilder_parabolic_sar_par -- Wilder PAR: close penetration of parabolic SAR signals reversal. trading_systems_and_methods_kaufman_perry_j_kaufma.

Stop-and-reverse using parabolic SAR: long when close > psar (SAR below price), short when close < psar.
Triggers on the bar when the relationship first flips (cross of close vs SAR).
Slight variation from wilder_parabolic_time_price_sar: uses the psar level directly vs close rather than the pre-computed direction flag alone.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "wilder_parabolic_sar_par",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,psar",
    "long": "close crosses above parabolic SAR (SAR previously above price) -> reverse to long",
    "short": "close crosses below psar -> reverse to short",
    "desc": "Wilder PAR: stop-and-reverse when close crosses the accelerating parabolic SAR level",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch21 Table21-12 PAR",
}


def signal(ind, pos, htf=None):
    """Close vs PSAR cross -> stop-and-reverse."""
    if pos < 1:
        return None
    c  = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    p  = ind["psar"][pos]
    p1 = ind["psar"][pos - 1]
    if nan(c, c1, p, p1):
        return None
    if c > p and c1 <= p1:
        return "long"
    if c < p and c1 >= p1:
        return "short"
    return None
