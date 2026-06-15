#!/usr/bin/env python3
"""trade_against_the_opening_opening_reversal_fade -- Fade the first directional move after the
session open: if the session opens higher than prior close, fade short; if lower, fade long.
Entry on the first bar after the open.

Source: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch.15 p.388-389.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "trade_against_the_opening_opening_reversal_fade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "day_open, prev_dhc, close",
    "long": "Today's session opened below prior day's close (weak open) -> fade long expecting reversal",
    "short": "Today's session opened above prior day's close (strong open) -> fade short expecting reversal",
    "desc": "Opening reversal fade: trade against the opening gap direction, expecting early-session mean reversion",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.15 p.388-389",
}


def signal(ind, pos, htf=None):
    """Fade the session open direction vs prior close."""
    d_open = ind["day_open"][pos]
    prev_c = ind["prev_dhc"][pos]
    c = ind["close"][pos]
    if nan(d_open, prev_c, c) or prev_c <= 0:
        return None
    # Only fire near the open (close is still near day_open = early session)
    # Use the distance from day_open as a proximity check
    a = ind["atr"][pos]
    if nan(a) or a <= 0:
        return None
    # Only signal if price hasn't moved far from day_open yet (within 0.5 ATR)
    if abs(c - d_open) > 0.5 * a:
        return None
    open_gap = d_open - prev_c
    if open_gap < 0:
        return "long"   # opened lower than prior close -> fade up
    if open_gap > 0:
        return "short"  # opened higher than prior close -> fade down
    return None
