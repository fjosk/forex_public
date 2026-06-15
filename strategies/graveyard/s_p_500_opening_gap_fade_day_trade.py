#!/usr/bin/env python3
"""s_p_500_opening_gap_fade_day_trade -- Fade an opening gap: if today opens above prior day's
high (gap up) -> short; if opens below prior day's low (gap down) -> long.

Source: elder_alexander_trading_for_a_living, Sec.22 p.101.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "s_p_500_opening_gap_fade_day_trade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "open, prev_dhh, prev_dll, rsi",
    "long": "open < prev_dll (gap down beyond prior-day low) AND RSI not still falling (rsi[0] >= rsi[1])",
    "short": "open > prev_dhh (gap up beyond prior-day high) AND RSI not still rising (rsi[0] <= rsi[1])",
    "desc": "Opening gap fade: gap below prior-day low -> long; gap above prior-day high -> short",
    "source": "elder_alexander_trading_for_a_living Sec.22 p.101",
}


def signal(ind, pos, htf=None):
    """Opening gap fade using prev_dhh / prev_dll."""
    if pos < 1:
        return None
    o = ind["open"][pos]
    pdh = ind["prev_dhh"][pos]
    pdl = ind["prev_dll"][pos]
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    if nan(o, pdh, pdl, r, r1) or pdh <= pdl:
        return None
    # gap down: open < prior-day low; oscillator not still overshooting
    if o < pdl and r >= r1:
        return "long"
    # gap up: open > prior-day high; oscillator not still overshooting
    if o > pdh and r <= r1:
        return "short"
    return None
