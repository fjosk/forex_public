#!/usr/bin/env python3
"""oops_signal_gap_fade_reversal -- Oops gap-fade reversal variant (from j_person index entry).
j_person_a_complete_guide_to_technical_trading_tac.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "oops_signal_gap_fade_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "fade",
    "tf": "1h-4h",
    "indicators": "open, high, low, prev_dhh, prev_dll",
    "long": "open < prev_dll (gap-down) AND high crosses back above prev_dll",
    "short": "open > prev_dhh (gap-up) AND low crosses back below prev_dhh",
    "desc": "Oops reversal: gap beyond prior-day extreme then price re-enters prior range",
    "source": "book: j_person_a_complete_guide_to_technical_trading_tac",
}


def signal(ind, pos, htf=None):
    """Gap fade using high/low crossing back through prior-day extreme."""
    o = ind["open"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    pdh = ind["prev_dhh"][pos]
    pdl = ind["prev_dll"][pos]
    if nan(o, h, lo, pdh, pdl):
        return None
    # Gap-down open; intraday high re-enters above prior-day low -> long
    if o < pdl and h > pdl:
        return "long"
    # Gap-up open; intraday low re-enters below prior-day high -> short
    if o > pdh and lo < pdh:
        return "short"
    return None
