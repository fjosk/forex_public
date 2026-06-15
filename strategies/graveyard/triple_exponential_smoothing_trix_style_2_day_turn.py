#!/usr/bin/env python3
"""triple_exponential_smoothing_trix_turn -- Hutson/TRIX: triple smoothed series rising/falling 2 bars. trading_systems_and_methods_kaufman_perry_j_kaufma.

TRIX = rate of change of EMA(EMA(EMA(close))) = triple-smoothed momentum.
Long: TRIX > 0 for 2 consecutive bars (series has risen 2 days).
Short: TRIX < 0 for 2 consecutive bars (series has fallen 2 days).
Reverse on opposite 2-bar direction signal.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "triple_exponential_smoothing_trix_style_2_day_turn",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "trix",
    "long": "TRIX positive for 2 consecutive bars (triple-smoothed series rising 2 days)",
    "short": "TRIX negative for 2 consecutive bars",
    "desc": "Hutson triple-smoothing 2-day turn: TRIX direction for 2 bars triggers entry",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch2 Triple Exponential Smoothing Hutson 1983",
}


def signal(ind, pos, htf=None):
    """TRIX positive/negative for 2 consecutive bars -> long/short."""
    if pos < 2:
        return None
    t  = ind["trix"][pos]
    t1 = ind["trix"][pos - 1]
    t2 = ind["trix"][pos - 2]
    if nan(t, t1, t2):
        return None
    # Rising 2 days: trix > 0 now and 1 bar ago; was not both positive 2 bars ago
    if t > 0 and t1 > 0 and not (t2 > 0 and t1 > 0):
        return "long"
    if t < 0 and t1 < 0 and not (t2 < 0 and t1 < 0):
        return "short"
    return None
