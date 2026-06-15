#!/usr/bin/env python3
"""oops_gap_fade_reversal -- Williams Oops! opening gap fade reversal. long_term_secrets_to_short_term_trading.

Open below prior low -> buy when close reclaims prior low (gap fills back up).
Open above prior high -> sell when close falls back below prior high.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "oops_gap_fade_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "1h-4h",
    "indicators": "open,close,prev_dhh,prev_dll",
    "long": "open < prev_dll (gap down outside prior range) AND close >= prev_dll (price recovers back to prior low)",
    "short": "open > prev_dhh (gap up outside prior range) AND close <= prev_dhh (price falls back to prior high)",
    "desc": "Oops! gap-fade reversal: gap open outside prior day range fades back to the prior extreme",
    "source": "long_term_secrets_to_short_term_trading, Ch7 pp.114-117",
}


def signal(ind, pos, htf=None):
    """Oops! gap-fade signal: open outside prior range, close returns to boundary."""
    if pos < 1:
        return None
    op = ind["open"][pos]
    c = ind["close"][pos]
    dhh = ind["prev_dhh"][pos]
    dll = ind["prev_dll"][pos]
    if nan(op, c, dhh, dll):
        return None
    # Gap down: open below prior day low, then price closes back at or above prior low
    if op < dll and c >= dll:
        return "long"
    # Gap up: open above prior day high, then price closes back at or below prior high
    if op > dhh and c <= dhh:
        return "short"
    return None
