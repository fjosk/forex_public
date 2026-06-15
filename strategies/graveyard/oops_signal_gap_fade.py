#!/usr/bin/env python3
"""oops_signal_gap_fade -- Larry Williams Oops: gap-fade when open gaps beyond prior day H/L.
j_person_a_complete_guide_to_technical_trading_tac.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "oops_signal_gap_fade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "fade",
    "tf": "1h-4h",
    "indicators": "open, prev_dhh, prev_dll",
    "long": "open < prev_dll (gap below prior low) AND close re-enters above prev_dll",
    "short": "open > prev_dhh (gap above prior high) AND close re-enters below prev_dhh",
    "desc": "Oops gap-fade: session open gaps beyond prior day high/low, fade the gap",
    "source": "book: j_person_a_complete_guide_to_technical_trading_tac",
}


def signal(ind, pos, htf=None):
    """Gap-down open with close recovering above prior-day low (buy Oops) or reverse."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    pdh = ind["prev_dhh"][pos]
    pdl = ind["prev_dll"][pos]
    if nan(c, o, pdh, pdl):
        return None
    # Gap down open then close re-enters above prior low -> long
    if o < pdl and c > pdl:
        return "long"
    # Gap up open then close re-enters below prior high -> short
    if o > pdh and c < pdh:
        return "short"
    return None
