#!/usr/bin/env python3
"""gap_up_sell_gap_pullback_buy -- Opening gap: if no pullback sell; if pullback occurs buy. trading_systems_and_methods_kaufman."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "gap_up_sell_gap_pullback_buy_opening_gap_continuation",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "open, high, low, prev_dlc",
    "long": "gap up day: low < open (pullback occurred) -> buy the pullback",
    "short": "gap up day: low >= open (no pullback, continued higher) -> fade sell",
    "desc": "Opening gap continuation: gap-up with no pullback -> fade short; gap-up with pullback -> buy the dip",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Gap-up analysis: pullback = long, no-pullback continuation = short."""
    if pos < 2:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    pc = ind["prev_dlc"][pos]
    if nan(o, h, l, pc):
        return None
    gap = o - pc
    # Only act on meaningful up gap (> 0)
    if gap <= 0:
        return None
    # Pullback: low dipped below or touched open
    if l < o:
        return "long"
    # No pullback: high kept going, low stayed above open -> fade (expect reversal back to open)
    if l >= o:
        return "short"
    return None
