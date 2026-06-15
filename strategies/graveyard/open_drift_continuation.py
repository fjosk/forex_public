#!/usr/bin/env python3
"""open_drift_continuation -- Opening-drift continuation: a moderate, ATR-normalized session gap that price keeps drifting in tends to continue.. tier2 (book-extracted from sister-lab catalog_books).

book:seasonality-time. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "open_drift_continuation",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "seasonality-time",
    "tf": "1h-4h",
    "indicators": "day_open, prev_dlc, close, ATR",
    "long": "Session opened 0.3-1.5 ATR above prior-day close and price holds above the open -- follow the gap up",
    "short": "Session opened 0.3-1.5 ATR below prior-day close and price holds below the open -- follow the gap down",
    "desc": "Opening-drift continuation: a moderate, ATR-normalized session gap that price keeps drifting in tends to continue.",
    "source": "book:seasonality-time",
}


def signal(I, i, htf=None):
    do, plc, c, a = I["day_open"][i], I["prev_dlc"][i], I["close"][i], I["atr"][i]
    if _nan(do, plc, c, a) or a <= 0:
        return None
    gap_atr = (do - plc) / a
    if 0.3 <= gap_atr <= 1.5 and c > do:
        return "long"
    if -1.5 <= gap_atr <= -0.3 and c < do:
        return "short"
    return None
