#!/usr/bin/env python3
"""breaking_high_breaking_low_n_day_breakout -- N-day Donchian high/low breakout (BCA Sekuritas manual). buku_panduan."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "breaking_high_breaking_low_n_day_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, high, low",
    "long": "high exceeds prior N-day Donchian upper (new N-day high)",
    "short": "low falls below prior N-day Donchian lower (new N-day low)",
    "desc": "Breaking High / Breaking Low: Donchian N-day extreme breakout from BCA Sekuritas manual",
    "source": "buku_panduan",
}


def signal(ind, pos, htf=None):
    """Donchian N-day high/low breakout signal."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, l, dc_up, dc_lo):
        return None
    if h > dc_up:
        return "long"
    if l < dc_lo:
        return "short"
    return None
