#!/usr/bin/env python3
"""gold_seasonality_calendar -- Gold seasonality calendar windows (Sahm Capital 20yr study).

Three rule-based windows on XAUUSD:
  W1 long:  January (month transition to 1)
  W2 short: transition into April (month transition to 4)
  W3 long:  transition into July (month transition to 7)
  Flat:     September-December (month in [9,10,11,12]) -- no new positions.
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "gold_seasonality_calendar",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "open_time, atr, dow",
    "long": "first bar of January (W1) or first bar of July (W3)",
    "short": "first bar of April (W2 short window)",
    "desc": "Gold seasonality calendar: Jan long / Apr short / Jul long windows (Sahm Capital 63% WR)",
    "source": "web:https://www.sahmcapital.com/news/content/how-to-trade-gold-seasonality-a-profitable-strategy-based-on-20-years-of-historical-data-2025-12-11",
}


def signal(ind, pos, htf=None):
    """Gold seasonality calendar windows."""
    ts0 = ind["open_time"][pos]
    ts1 = ind["open_time"][pos - 1]
    if nan(ts0, ts1):
        return None
    dt0 = datetime.datetime.utcfromtimestamp(ts0 / 1000)
    dt1 = datetime.datetime.utcfromtimestamp(ts1 / 1000)
    m0 = dt0.month
    m1 = dt1.month
    # Flat in Sep-Dec: no new positions
    if m0 in (9, 10, 11, 12):
        return None
    # Only fire on month transition
    if m0 == m1:
        return None
    if m0 == 1:   # Window 1: January long
        return "long"
    if m0 == 4:   # Window 2: April short
        return "short"
    if m0 == 7:   # Window 3: July long
        return "long"
    return None
