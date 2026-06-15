#!/usr/bin/env python3
"""high_tight_flag_break -- High-and-tight flag: requires a near-double run then a shallow tight pullback, entering long on the flag-high breakout (long-only setup).. tier2 (book-extracted from sister-lab catalog_books).

book:breakout. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "high_tight_flag_break",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "OHLC (rolling windows)",
    "long": "After a ~90%+ run off the base low, a tight (<=25%) consolidation breaks above the 8-bar flag high",
    "short": "## Indicators",
    "desc": "High-and-tight flag: requires a near-double run then a shallow tight pullback, entering long on the flag-high breakout (long-only setup).",
    "source": "book:breakout",
}


def signal(I, i, htf=None):
    if i < 61:
        return None
    h, l, c = I["high"], I["low"], I["close"]
    if _nan(c[i]):
        return None
    base_win = [l[k] for k in range(i-60, i-20)]
    swing_win = [h[k] for k in range(i-20, i-2)]
    flag_h_win = [h[k] for k in range(i-8, i)]
    flag_l_win = [l[k] for k in range(i-8, i)]
    if any(_nan(x) for x in base_win) or any(_nan(x) for x in swing_win) \
            or any(_nan(x) for x in flag_h_win) or any(_nan(x) for x in flag_l_win):
        return None
    base_lo = min(base_win)
    if base_lo == 0:
        return None
    swing_hi = max(swing_win)
    if swing_hi == 0:
        return None
    doubled = (swing_hi - base_lo) / base_lo >= 0.90
    flag_hi = max(flag_h_win)
    flag_lo = min(flag_l_win)
    tight = (swing_hi - flag_lo) / swing_hi <= 0.25
    if doubled and tight and c[i] > flag_hi:
        return "long"
    return None
