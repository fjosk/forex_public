#!/usr/bin/env python3
"""crude_oil_spring_seasonal -- WTI crude oil spring seasonal long (Feb-Sep). Academic study 1983-2017.

Long: enter on first bar of February (month == 2 AND prior month != 2).
Short (optional, weaker): enter on first bar of October.
Uses open_time epoch-ms for calendar month extraction.
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "crude_oil_spring_seasonal",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "open_time, atr",
    "long": "first bar of February (month transition to 2): long WTI seasonal",
    "short": "first bar of October (month transition to 10): optional short window",
    "desc": "WTI crude oil spring seasonal: long Feb-Sep, optional short Oct-Jan",
    "source": "web:https://www.jois.eu/files/12_547_Arendas%20et%20al.pdf",
}


def signal(ind, pos, htf=None):
    """Crude oil spring seasonal entry."""
    ts0 = ind["open_time"][pos]
    ts1 = ind["open_time"][pos - 1]
    if nan(ts0, ts1):
        return None
    dt0 = datetime.datetime.utcfromtimestamp(ts0 / 1000)
    dt1 = datetime.datetime.utcfromtimestamp(ts1 / 1000)
    m0 = dt0.month
    m1 = dt1.month
    # Only fire on the month transition (first bar of a new month)
    if m0 == m1:
        return None
    if m0 == 2:
        return "long"
    if m0 == 10:
        return "short"
    return None
