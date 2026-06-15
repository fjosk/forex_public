#!/usr/bin/env python3
"""first_hour_range_breakout_adr -- First 60-minute session range breakout with ATR-based exit. trading_systems_and_methods_kaufman."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "first_hour_60_minute_range_breakout_with_adr_exit",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "prev_dhh, prev_dll, atr, open, high, low, hour_utc",
    "long": "high breaks above prev_dhh (proxy for first-hour high) after the first hour has elapsed",
    "short": "low breaks below prev_dll (proxy for first-hour low) after the first hour has elapsed",
    "desc": "First-hour range breakout with ADR exit; proxy: prior-day H/L as session reference range",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Break above/below prior-day H/L after session open (hour_utc >= 1 as post-first-hour proxy)."""
    if pos < 2:
        return None
    hr = ind["hour_utc"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    ph = ind["prev_dhh"][pos]
    pl = ind["prev_dll"][pos]
    if nan(hr, h, l, ph, pl):
        return None
    # Act only after first hour of the major FX session (NY open ~13 UTC or London ~8 UTC)
    # Proxy: post-hour 0 i.e. hour >= 1 and before end of session (hour < 21)
    if hr < 1 or hr >= 21:
        return None
    if h > ph:
        return "long"
    if l < pl:
        return "short"
    return None
