#!/usr/bin/env python3
"""rising_falling_three -- five-bar continuation: impulse bar, three-bar inside consolidation, then a resume bar breaking the impulse close. tier2 (book-extracted from sister-lab catalog_books).

book:candlestick. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "rising_falling_three",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ohlc",
    "long": "long trend bar (i-4), three small bars inside its range, then close beyond the trend bar close (rising three)",
    "short": "long down bar, three small inside bars, then close below the trend bar close (falling three)",
    "desc": "five-bar continuation: impulse bar, three-bar inside consolidation, then a resume bar breaking the impulse close",
    "source": "book:candlestick",
}


def signal(I, i, htf=None):
    if i < 4:
        return None
    o4 = I['open'][i-4]; c4 = I['close'][i-4]
    h4 = I['high'][i-4]; l4 = I['low'][i-4]
    c = I['close'][i]
    vals = [o4, c4, h4, l4, c]
    for j in (i-3, i-2, i-1):
        vals.extend([I['open'][j], I['close'][j], I['high'][j], I['low'][j]])
    if _nan(*vals):
        return None
    b0 = abs(c4 - o4)
    small = all(abs(I['close'][j] - I['open'][j]) < 0.5 * b0 for j in (i-3, i-2, i-1))
    inside = all(I['high'][j] <= h4 and I['low'][j] >= l4 for j in (i-3, i-2, i-1))
    if c4 > o4 and small and inside and c > c4:
        return 'long'
    if c4 < o4 and small and inside and c < c4:
        return 'short'
    return None
