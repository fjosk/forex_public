#!/usr/bin/env python3
"""dow_two_day_reversal -- Day-of-Week Two-Day-Run Reversal: fade a 2-bar directional run when the bar lands on Wednesday or Thursday (UTC weekday).. tier2 (book-extracted from sister-lab catalog_books).

book:seasonality-time. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "dow_two_day_reversal",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "seasonality",
    "tf": "1d",
    "indicators": "Close, day-of-week (Mon=0..Sun=6 UTC)",
    "long": "Two-down-bar run faded into mid-week (Wed/Thu)",
    "short": "Two-up-bar run faded into mid-week (Wed/Thu)",
    "desc": "Day-of-Week Two-Day-Run Reversal: fade a 2-bar directional run when the bar lands on Wednesday or Thursday (UTC weekday).",
    "source": "book:seasonality-time",
}


def signal(I, i, htf=None):
    if i < 2:
        return None
    c, c1, c2 = I["close"][i], I["close"][i-1], I["close"][i-2]
    d = I["dow"][i]
    if _nan(c, c1, c2, d):
        return None
    up_today = c > c1
    up_yest = c1 > c2
    two_day_up = up_today and up_yest
    two_day_down = (not up_today) and (not up_yest)
    # dow = ISO weekday Mon=0..Sun=6 (UTC). Only fade mid-week (Wed=2, Thu=3).
    if d in (2.0, 3.0):
        if two_day_up:
            return "short"
        if two_day_down:
            return "long"
    return None
