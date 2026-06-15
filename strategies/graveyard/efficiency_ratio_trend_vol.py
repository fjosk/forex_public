#!/usr/bin/env python3
"""efficiency_ratio_trend_vol -- Kaufman Efficiency Ratio regime trigger: when directional efficiency turns above 0.35 a trend is forming; take it in the direction of the EMA20 slope.. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "efficiency_ratio_trend_vol",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h-4h",
    "indicators": "close,ema20,eff_ratio",
    "long": "Kaufman efficiency ratio crosses up through 0.35 while EMA20 is rising",
    "short": "Kaufman efficiency ratio crosses up through 0.35 while EMA20 is falling",
    "desc": "Kaufman Efficiency Ratio regime trigger: when directional efficiency turns above 0.35 a trend is forming; take it in the direction of the EMA20 slope.",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    thr = 0.35
    er = I['eff_ratio'][i]; er1 = I['eff_ratio'][i-1]
    e = I['ema20'][i]; e1 = I['ema20'][i-1]
    if _nan(er, er1, e, e1):
        return None
    er_turn = er > thr and er1 <= thr
    if er_turn and e > e1:
        return 'long'
    if er_turn and e < e1:
        return 'short'
    return None
